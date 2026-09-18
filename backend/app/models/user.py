from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    hashed_password = Column(String(255), nullable=True)
    role = Column(String(30), default="requester")  # requester, donor, hospital, blood_bank, admin
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    donor_profile = relationship("DonorProfile", back_populates="user", uselist=False)
    emergency_requests = relationship("EmergencyRequest", back_populates="requester")

class DonorProfile(Base):
    __tablename__ = "donor_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    display_name = Column(String(100), nullable=False)
    blood_group = Column(String(10), nullable=False, index=True)  # A+, O+, etc.
    city = Column(String(100), default="Bhubaneswar")
    latitude = Column(Float, nullable=False, default=20.2961)
    longitude = Column(Float, nullable=False, default=85.8245)
    preferred_radius_km = Column(Float, default=10.0)
    is_available = Column(Boolean, default=True)
    emergency_notifications_enabled = Column(Boolean, default=True)
    last_donation_date = Column(DateTime, nullable=True)
    response_count = Column(Integer, default=0)
    acceptance_count = Column(Integer, default=0)

    user = relationship("User", back_populates="donor_profile")
