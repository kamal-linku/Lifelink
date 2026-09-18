from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class BloodInventoryItem(BaseModel):
    id: Optional[int] = None
    blood_group: str
    component: str
    units_available: int
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True

class BloodBankBase(BaseModel):
    name: str
    category: str = "Govt/Charitable"
    address: str
    city: str = "Bhubaneswar"
    latitude: float
    longitude: float
    contact_phone: str
    is_verified: bool = True
    operating_hours: str = "24x7"

class BloodBankResponse(BloodBankBase):
    id: int
    inventory: List[BloodInventoryItem] = []

    class Config:
        from_attributes = True

class HospitalBase(BaseModel):
    name: str
    registration_no: Optional[str] = None
    address: str
    city: str = "Bhubaneswar"
    latitude: float
    longitude: float
    emergency_contact: str
    is_verified: bool = True
    has_blood_bank: bool = False
    total_beds: int = 200
    icu_beds_available: int = 15

class HospitalResponse(HospitalBase):
    id: int

    class Config:
        from_attributes = True

class AmbulanceBase(BaseModel):
    vehicle_number: str
    provider_name: str
    ambulance_type: str = "Basic Life Support (BLS)"
    city: str = "Bhubaneswar"
    current_latitude: float
    current_longitude: float
    driver_name: str
    contact_phone: str
    is_available: bool = True
    is_verified: bool = True

class AmbulanceResponse(AmbulanceBase):
    id: int
    last_ping: datetime

    class Config:
        from_attributes = True

class PharmacyBase(BaseModel):
    name: str
    address: str
    city: str = "Bhubaneswar"
    latitude: float
    longitude: float
    contact_phone: str
    is_24x7: bool = True
    is_verified: bool = True
    inventory_notes: str = "Emergency medications, IV fluids"
    last_verified_minutes_ago: int = 10

class PharmacyResponse(PharmacyBase):
    id: int

    class Config:
        from_attributes = True
