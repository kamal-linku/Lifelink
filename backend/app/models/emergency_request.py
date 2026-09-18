from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class EmergencyRequest(Base):
    __tablename__ = "emergency_requests"

    id = Column(Integer, primary_key=True, index=True)
    request_code = Column(String(30), unique=True, index=True) # e.g. LL-2841
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    patient_name = Column(String(120), nullable=False)
    blood_group = Column(String(10), nullable=False, index=True)
    component = Column(String(50), default="Packed RBC")
    units_needed = Column(Integer, default=2)
    
    hospital_name = Column(String(150), nullable=False)
    city = Column(String(100), default="Bhubaneswar")
    latitude = Column(Float, nullable=False, default=20.2961)
    longitude = Column(Float, nullable=False, default=85.8245)
    
    urgency = Column(String(20), default="Critical") # Normal, Urgent, Critical
    required_within_hours = Column(Float, default=2.0)
    contact_phone = Column(String(30), nullable=False)
    additional_notes = Column(Text, nullable=True)
    
    # Workflow Status Engine: MATCHING -> CONTACTED -> RESPONDED -> CONFIRMED -> COMPLETED
    status = Column(String(30), default="MATCHING", index=True)
    assigned_resource_info = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    requester = relationship("User", back_populates="emergency_requests")
    matches = relationship("ResourceMatch", back_populates="request", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="request", cascade="all, delete-orphan")

class ResourceMatch(Base):
    __tablename__ = "resource_matches"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("emergency_requests.id"), nullable=False)
    resource_type = Column(String(30), nullable=False) # blood_bank, volunteer, hospital
    resource_id = Column(Integer, nullable=False)
    resource_name = Column(String(150), nullable=False)
    
    score = Column(Float, nullable=False) # 0 to 100%
    distance_km = Column(Float, nullable=False)
    availability_status = Column(String(50), default="CONFIRMED") # CONFIRMED, AVAILABLE, UNVERIFIED
    match_status = Column(String(30), default="NOTIFIED") # NOTIFIED, ACCEPTED, DECLINED, FULFILLED
    created_at = Column(DateTime, default=datetime.utcnow)

    request = relationship("EmergencyRequest", back_populates="matches")
