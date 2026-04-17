from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    class Config:
        orm_mode = True

class DonorProfileCreate(BaseModel):
    user_id: int
    blood_group: str
    latitude: float
    longitude: float
    phone_number: str

class DonorProfileOut(BaseModel):
    donor_id: str
    blood_group: str
    latitude: float
    longitude: float
    is_available: bool
    reliability_score: int
    class Config:
        orm_mode = True

class BloodRequestCreate(BaseModel):
    requester_id: int
    blood_group: str
    latitude: float
    longitude: float
    radius_km: float = 10.0

class BloodRequestOut(BaseModel):
    id: int
    blood_group: str
    status: str
    created_at: datetime
    class Config:
        orm_mode = True
