from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class EmergencyRequestCreate(BaseModel):
    patient_name: str
    blood_group: str
    component: str = "Packed RBC"
    units_needed: int = 2
    hospital_name: str
    city: str = "Bhubaneswar"
    latitude: float = 20.2961
    longitude: float = 85.8245
    urgency: str = "Critical" # Normal, Urgent, Critical
    required_within_hours: float = 2.0
    contact_phone: str
    additional_notes: Optional[str] = None

class ResourceMatchItem(BaseModel):
    id: Optional[int] = None
    resource_type: str # blood_bank, volunteer, hospital
    resource_id: int
    resource_name: str
    score: float # 0 - 100
    distance_km: float
    availability_status: str # CONFIRMED, AVAILABLE
    match_status: str
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    units_available: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True

class EmergencyRequestResponse(BaseModel):
    id: int
    request_code: str
    patient_name: str
    blood_group: str
    component: str
    units_needed: int
    hospital_name: str
    city: str
    latitude: float
    longitude: float
    urgency: str
    required_within_hours: float
    contact_phone: str
    additional_notes: Optional[str] = None
    status: str # MATCHING -> CONTACTED -> RESPONDED -> CONFIRMED -> COMPLETED
    assigned_resource_info: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    matches: List[ResourceMatchItem] = []

    class Config:
        from_attributes = True

class StatusUpdateRequest(BaseModel):
    status: str # MATCHING, CONTACTED, RESPONDED, CONFIRMED, COMPLETED, CANCELLED
    resource_info: Optional[str] = None
