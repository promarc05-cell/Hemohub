from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    donor_profile = relationship("DonorProfile", back_populates="user", uselist=False)

class DonorProfile(Base):
    __tablename__ = "donor_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    donor_id = Column(String, unique=True, default=lambda: str(uuid.uuid4())[:8].upper())
    blood_group = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    is_available = Column(Boolean, default=True)
    reliability_score = Column(Integer, default=100)
    last_donation_date = Column(DateTime, nullable=True)
    phone_number = Column(String) # Encrypted or masked in API
    
    user = relationship("User", back_populates="donor_profile")
    donations = relationship("DonationTransaction", back_populates="donor")

class BloodRequest(Base):
    __tablename__ = "blood_requests"
    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"))
    blood_group = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    radius_km = Column(Float, default=10.0)
    status = Column(String, default="OPEN") # OPEN, CLOSED, EMERGENCY
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    transactions = relationship("DonationTransaction", back_populates="request")

class DonationTransaction(Base):
    __tablename__ = "donation_transactions"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("blood_requests.id"))
    donor_id = Column(Integer, ForeignKey("donor_profiles.id"))
    status = Column(String, default="MATCHED") # MATCHED, CONFIRMED, COMPLETED, CANCELLED
    donor_confirmed = Column(Boolean, default=False)
    requester_confirmed = Column(Boolean, default=False)
    
    request = relationship("BloodRequest", back_populates="transactions")
    donor = relationship("DonorProfile", back_populates="donations")
    blood_unit = relationship("BloodUnit", back_populates="transaction", uselist=False)

class BloodUnit(Base):
    __tablename__ = "blood_units"
    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(String, unique=True, default=lambda: f"UNIT-{uuid.uuid4().hex[:8].upper()}")
    transaction_id = Column(Integer, ForeignKey("donation_transactions.id"))
    status = Column(String, default="COLLECTED") # COLLECTED, TESTING, STORAGE, IN_TRANSIT, DELIVERED
    current_location = Column(String)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    transaction = relationship("DonationTransaction", back_populates="blood_unit")
