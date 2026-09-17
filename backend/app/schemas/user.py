from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    role: str = "requester"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

class DonorProfileBase(BaseModel):
    display_name: str
    blood_group: str
    city: str = "Bhubaneswar"
    latitude: float = 20.2961
    longitude: float = 85.8245
    preferred_radius_km: float = 10.0
    is_available: bool = True
    emergency_notifications_enabled: bool = True

class DonorProfileCreate(DonorProfileBase):
    phone: str
    email: str

class DonorProfileResponse(DonorProfileBase):
    id: int
    user_id: Optional[int]
    response_count: int
    acceptance_count: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
