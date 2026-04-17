from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, matching
from database import engine, get_db
import uuid

# Initialize Database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blood Donation Platform API")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = models.User(email=user.email, hashed_password=user.password) # In real app, hash password
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/donors/", response_model=schemas.DonorProfileOut)
def create_donor_profile(profile: schemas.DonorProfileCreate, db: Session = Depends(get_db)):
    new_profile = models.DonorProfile(**profile.dict())
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

@app.post("/requests/", response_model=schemas.BloodRequestOut)
def create_blood_request(req: schemas.BloodRequestCreate, db: Session = Depends(get_db)):
    new_req = models.BloodRequest(**req.dict())
    db.add(new_req)
    db.commit()
    db.refresh(new_req)
    
    # Trigger matching logic
    donors = db.query(models.DonorProfile).all()
    matches = matching.find_nearby_donors(
        new_req.latitude, new_req.longitude, donors, new_req.radius_km, new_req.blood_group
    )
    
    # Store initial matches as transactions
    for match in matches:
        donor = db.query(models.DonorProfile).filter(models.DonorProfile.donor_id == match['donor_id']).first()
        transaction = models.DonationTransaction(request_id=new_req.id, donor_id=donor.id)
        db.add(transaction)
    
    db.commit()
    return new_req

@app.get("/requests/{request_id}/matches")
def get_matches(request_id: int, db: Session = Depends(get_db)):
    transactions = db.query(models.DonationTransaction).filter(models.DonationTransaction.request_id == request_id).all()
    results = []
    for tx in transactions:
        donor = tx.donor
        # Privacy Logic: Mask phone unless mutual confirmation
        phone = donor.phone_number if (tx.donor_confirmed and tx.requester_confirmed) else "********"
        
        results.append({
            "transaction_id": tx.id,
            "donor_id": donor.donor_id,
            "blood_group": donor.blood_group,
            "reliability_score": donor.reliability_score,
            "phone": phone,
            "status": tx.status,
            "confirmed": {"donor": tx.donor_confirmed, "requester": tx.requester_confirmed}
        })
    return results

@app.post("/transactions/{tx_id}/confirm")
def confirm_donation(tx_id: int, side: str, db: Session = Depends(get_db)):
    tx = db.query(models.DonationTransaction).filter(models.DonationTransaction.id == tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    if side == "donor":
        tx.donor_confirmed = True
    elif side == "requester":
        tx.requester_confirmed = True
    
    if tx.donor_confirmed and tx.requester_confirmed:
        tx.status = "CONFIRMED"
        # Create blood unit for tracking
        new_unit = models.BloodUnit(transaction_id=tx.id)
        db.add(new_unit)
        
    db.commit()
    return {"status": "success", "tx_status": tx.status}

@app.get("/trace/{unit_id}")
def trace_blood_unit(unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(models.BloodUnit).filter(models.BloodUnit.unit_id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Blood unit not found")
    
    return {
        "unit_id": unit.unit_id,
        "status": unit.status,
        "location": unit.current_location,
        "updated_at": unit.updated_at,
        "history": [
            {"status": "COLLECTED", "time": unit.updated_at},
        ]
    }

@app.get("/emergencies")
def get_emergencies(db: Session = Depends(get_db)):
    # Prioritizes requests from highly reliable donors
    requests = db.query(models.BloodRequest).filter(models.BloodRequest.status != "CLOSED").all()
    results = []
    for req in requests:
        # Check if the requester is also a donor to boost their priority
        priority = 0
        requester_donor = db.query(models.DonorProfile).filter(models.DonorProfile.user_id == req.requester_id).first()
        if requester_donor:
            priority = requester_donor.reliability_score
            
        results.append({
            "request_id": req.id,
            "blood_group": req.blood_group,
            "latitude": req.latitude,
            "longitude": req.longitude,
            "priority": priority, # Top score donors prioritized
            "distance": round(req.radius_km, 2)
        })
        
    # Sort descending by priority
    results.sort(key=lambda x: x['priority'], reverse=True)
    return results
