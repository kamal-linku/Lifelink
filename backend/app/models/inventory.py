from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class BloodInventory(Base):
    __tablename__ = "blood_inventory"

    id = Column(Integer, primary_key=True, index=True)
    blood_bank_id = Column(Integer, ForeignKey("blood_banks.id"), nullable=False)
    blood_group = Column(String(10), nullable=False, index=True) # A+, O-, etc.
    component = Column(String(50), nullable=False, default="Packed RBC") # Packed RBC, Platelets, Plasma, Whole Blood
    units_available = Column(Integer, nullable=False, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("blood_bank_id", "blood_group", "component", name="uq_bank_group_component"),
    )

    blood_bank = relationship("BloodBank", back_populates="inventory")
