from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.resource import BloodBank, Hospital, Ambulance, Pharmacy
from app.models.user import DonorProfile
from app.models.inventory import BloodInventory
from app.schemas.resource import (
    BloodBankResponse,
    HospitalResponse,
    AmbulanceResponse,
    PharmacyResponse
)

router = APIRouter(prefix="/api/resources", tags=["Emergency Resources"])

@router.get("/map")
def get_map_resources(
    blood_group: Optional[str] = None,
    resource_type: Optional[str] = None, # all, hospital, blood_bank, ambulance, volunteer
    db: Session = Depends(get_db)
):
    """
    Unified Geo-JSON style response for Leaflet Interactive Radar.
    """
    markers = []

    # 1. Hospitals
    if not resource_type or resource_type in ["all", "hospital"]:
        hospitals = db.query(Hospital).all()
        for h in hospitals:
            markers.append({
                "id": f"hosp_{h.id}",
                "type": "hospital",
                "name": h.name,
                "latitude": h.latitude,
                "longitude": h.longitude,
                "address": h.address,
                "contact": h.emergency_contact,
                "status": "Operational",
                "details": {
                    "total_beds": h.total_beds,
                    "icu_available": h.icu_beds_available,
                    "has_blood_bank": h.has_blood_bank
                },
                "is_verified": h.is_verified
            })

    # 2. Blood Banks
    if not resource_type or resource_type in ["all", "blood_bank"]:
        blood_banks = db.query(BloodBank).all()
        for bb in blood_banks:
            # Query stock
            inv_query = db.query(BloodInventory).filter(BloodInventory.blood_bank_id == bb.id)
            if blood_group:
                inv_query = inv_query.filter(BloodInventory.blood_group == blood_group.upper())
            inventories = inv_query.all()
            stock_summary = {f"{i.blood_group}_{i.component}": i.units_available for i in inventories}
            total_units = sum(i.units_available for i in inventories)

            markers.append({
                "id": f"bank_{bb.id}",
                "type": "blood_bank",
                "name": bb.name,
                "category": bb.category,
                "latitude": bb.latitude,
                "longitude": bb.longitude,
                "address": bb.address,
                "contact": bb.contact_phone,
                "status": f"{total_units} Units Available",
                "details": {
                    "operating_hours": bb.operating_hours,
                    "stock": stock_summary,
                    "total_units": total_units
                },
                "is_verified": bb.is_verified
            })

    # 3. Ambulances
    if not resource_type or resource_type in ["all", "ambulance"]:
        ambulances = db.query(Ambulance).all()
        for a in ambulances:
            markers.append({
                "id": f"amb_{a.id}",
                "type": "ambulance",
                "name": f"{a.provider_name} ({a.vehicle_number})",
                "latitude": a.current_latitude,
                "longitude": a.current_longitude,
                "contact": a.contact_phone,
                "status": "Available" if a.is_available else "Dispatched",
                "details": {
                    "ambulance_type": a.ambulance_type,
                    "driver_name": a.driver_name,
                    "is_available": a.is_available
                },
                "is_verified": a.is_verified
            })

    # 4. Verified Volunteers
    if not resource_type or resource_type in ["all", "volunteer"]:
        donor_query = db.query(DonorProfile).filter(DonorProfile.is_available == True)
        if blood_group:
            donor_query = donor_query.filter(DonorProfile.blood_group == blood_group.upper())
        donors = donor_query.all()
        for d in donors:
            markers.append({
                "id": f"donor_{d.id}",
                "type": "volunteer",
                "name": f"Donor {d.display_name}",
                "latitude": d.latitude,
                "longitude": d.longitude,
                "contact": "Secure Masked Call",
                "status": f"{d.blood_group} Available",
                "details": {
                    "blood_group": d.blood_group,
                    "city": d.city,
                    "preferred_radius_km": d.preferred_radius_km
                },
                "is_verified": True
            })

    return markers

@router.get("/blood-banks", response_model=List[BloodBankResponse])
def list_blood_banks(db: Session = Depends(get_db)):
    return db.query(BloodBank).all()

@router.get("/hospitals", response_model=List[HospitalResponse])
def list_hospitals(db: Session = Depends(get_db)):
    return db.query(Hospital).all()

@router.get("/ambulances", response_model=List[AmbulanceResponse])
def list_ambulances(db: Session = Depends(get_db)):
    return db.query(Ambulance).all()

@router.get("/pharmacies", response_model=List[PharmacyResponse])
def list_pharmacies(db: Session = Depends(get_db)):
    return db.query(Pharmacy).all()
