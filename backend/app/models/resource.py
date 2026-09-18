from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class BloodBank(Base):
    __tablename__ = "blood_banks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    license_no = Column(String(50), nullable=True)
    category = Column(String(50), default="Govt/Charitable")  # Govt, Red Cross, Private
    address = Column(String(255), nullable=False)
    city = Column(String(100), default="Bhubaneswar")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    contact_phone = Column(String(30), nullable=False)
    contact_email = Column(String(100), nullable=True)
    is_verified = Column(Boolean, default=True)
    operating_hours = Column(String(50), default="24x7")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    inventory = relationship("BloodInventory", back_populates="blood_bank")

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    registration_no = Column(String(50), nullable=True)
    address = Column(String(255), nullable=False)
    city = Column(String(100), default="Bhubaneswar")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    emergency_contact = Column(String(30), nullable=False)
    is_verified = Column(Boolean, default=True)
    has_blood_bank = Column(Boolean, default=False)
    total_beds = Column(Integer, default=200)
    icu_beds_available = Column(Integer, default=15)
    created_at = Column(DateTime, default=datetime.utcnow)

class Ambulance(Base):
    __tablename__ = "ambulances"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_number = Column(String(30), unique=True, nullable=False)
    provider_name = Column(String(100), nullable=False)
    ambulance_type = Column(String(50), default="Basic Life Support (BLS)") # BLS, ALS, Patient Transport
    city = Column(String(100), default="Bhubaneswar")
    current_latitude = Column(Float, nullable=False)
    current_longitude = Column(Float, nullable=False)
    driver_name = Column(String(100), nullable=False)
    contact_phone = Column(String(30), nullable=False)
    is_available = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=True)
    last_ping = Column(DateTime, default=datetime.utcnow)

class Pharmacy(Base):
    __tablename__ = "pharmacies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(100), default="Bhubaneswar")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    contact_phone = Column(String(30), nullable=False)
    is_24x7 = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=True)
    inventory_notes = Column(String(500), default="Critical emergency drugs, coagulants, IV fluids")
    last_verified_minutes_ago = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.utcnow)
