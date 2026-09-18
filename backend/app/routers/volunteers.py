from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, DonorProfile
from app.models.emergency_request import EmergencyRequest, ResourceMatch
from app.schemas.user import DonorProfileCreate, DonorProfileResponse
from app.services.websocket_manager import manager

router = APIRouter(prefix="/api/volunteers", tags=["Volunteers"])

@router.post("/register", response_model=DonorProfileResponse)
def register_volunteer(payload: DonorProfileCreate, db: Session = Depends(get_db)):
    # Create user account
    user = User(
        name=payload.display_name,
        email=payload.email,
        phone=payload.phone,
        role="donor",
        is_verified=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    donor = DonorProfile(
        user_id=user.id,
        display_name=payload.display_name,
        blood_group=payload.blood_group.upper(),
        city=payload.city,
        latitude=payload.latitude,
        longitude=payload.longitude,
        preferred_radius_km=payload.preferred_radius_km,
        is_available=payload.is_available,
        emergency_notifications_enabled=payload.emergency_notifications_enabled
    )
    db.add(donor)
    db.commit()
    db.refresh(donor)
    return donor

@router.get("/all")
def get_all_volunteers(db: Session = Depends(get_db)):
    donors = db.query(DonorProfile).all()
    # Note: Strip private phone and email to guarantee volunteer privacy
    results = []
    for d in donors:
        results.append({
            "id": d.id,
            "display_name": d.display_name,
            "blood_group": d.blood_group,
            "city": d.city,
            "latitude": d.latitude,
            "longitude": d.longitude,
            "is_available": d.is_available,
            "preferred_radius_km": d.preferred_radius_km,
            "response_count": d.response_count,
            "acceptance_count": d.acceptance_count
        })
    return results

@router.patch("/{donor_id}/availability")
async def toggle_availability(donor_id: int, is_available: bool, db: Session = Depends(get_db)):
    donor = db.query(DonorProfile).filter(DonorProfile.id == donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    
    donor.is_available = is_available
    db.commit()

    # WS event
    await manager.broadcast({
        "event": "DONOR_AVAILABILITY_CHANGED",
        "donor_id": donor.id,
        "display_name": donor.display_name,
        "is_available": donor.is_available
    })
    return {"message": "Availability updated", "is_available": donor.is_available}

@router.post("/{donor_id}/respond")
async def volunteer_respond(
    donor_id: int,
    request_code: str,
    action: str, # "ACCEPT" or "DECLINE"
    db: Session = Depends(get_db)
):
    donor = db.query(DonorProfile).filter(DonorProfile.id == donor_id).first()
    req = db.query(EmergencyRequest).filter(EmergencyRequest.request_code == request_code.upper()).first()
    if not donor or not req:
        raise HTTPException(status_code=404, detail="Donor or Emergency Request not found")

    donor.response_count += 1
    if action.upper() == "ACCEPT":
        donor.acceptance_count += 1
        # Update request status to RESPONDED if still MATCHING or CONTACTED
        if req.status in ["MATCHING", "CONTACTED"]:
            req.status = "RESPONDED"
            req.assigned_resource_info = f"Volunteer Donor ({donor.display_name} - {donor.blood_group})"
            db.commit()

        # Secure masked contact token (never expose raw phone)
        masked_contact_token = f"SECURE-BRIDGE-{donor.id}-{req.id}"

        # Real-time WebSocket announcement
        await manager.broadcast({
            "event": "VOLUNTEER_ACCEPTED",
            "request_code": req.request_code,
            "donor_display_name": donor.display_name,
            "blood_group": donor.blood_group,
            "new_status": req.status,
            "masked_contact_token": masked_contact_token
        })

        return {
            "status": "ACCEPTED",
            "message": f"Thank you {donor.display_name}! The requester has been notified.",
            "secure_token": masked_contact_token,
            "hospital": req.hospital_name
        }
    else:
        db.commit()
        return {"status": "DECLINED", "message": "Request declined"}
