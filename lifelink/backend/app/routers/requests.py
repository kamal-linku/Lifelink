import random
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.emergency_request import EmergencyRequest, ResourceMatch
from app.schemas.request import (
    EmergencyRequestCreate,
    EmergencyRequestResponse,
    StatusUpdateRequest,
    ResourceMatchItem
)
from app.services.matching_engine import find_ranked_matches_for_request
from app.services.websocket_manager import manager

router = APIRouter(prefix="/api/requests", tags=["Emergency Requests"])

def generate_request_code() -> str:
    return f"LL-{random.randint(1000, 9999)}"

@router.post("/", response_model=EmergencyRequestResponse)
async def create_emergency_request(
    payload: EmergencyRequestCreate,
    db: Session = Depends(get_db)
):
    code = generate_request_code()
    # Ensure code uniqueness
    while db.query(EmergencyRequest).filter(EmergencyRequest.request_code == code).first():
        code = generate_request_code()

    req = EmergencyRequest(
        request_code=code,
        patient_name=payload.patient_name,
        blood_group=payload.blood_group.upper(),
        component=payload.component,
        units_needed=payload.units_needed,
        hospital_name=payload.hospital_name,
        city=payload.city,
        latitude=payload.latitude,
        longitude=payload.longitude,
        urgency=payload.urgency,
        required_within_hours=payload.required_within_hours,
        contact_phone=payload.contact_phone,
        additional_notes=payload.additional_notes,
        status="MATCHING"
    )
    db.add(req)
    db.commit()
    db.refresh(req)

    # Trigger Matching Engine
    ranked_matches = find_ranked_matches_for_request(db, req)

    # Persist top 10 matches
    persisted_matches = []
    for m in ranked_matches[:10]:
        rm = ResourceMatch(
            request_id=req.id,
            resource_type=m["resource_type"],
            resource_id=m["resource_id"],
            resource_name=m["resource_name"],
            score=m["score"],
            distance_km=m["distance_km"],
            availability_status=m["availability_status"],
            match_status="NOTIFIED"
        )
        db.add(rm)
        persisted_matches.append(rm)
    db.commit()

    # Real-time WebSocket Broadcast
    event_payload = {
        "event": "EMERGENCY_CREATED",
        "request_code": req.request_code,
        "patient_name": req.patient_name,
        "blood_group": req.blood_group,
        "component": req.component,
        "units": req.units_needed,
        "hospital": req.hospital_name,
        "urgency": req.urgency,
        "matches_found": len(ranked_matches),
        "timestamp": req.created_at.isoformat()
    }
    await manager.broadcast(event_payload)

    # Construct response with enriched match details
    response_matches = []
    for m in ranked_matches[:10]:
        response_matches.append(ResourceMatchItem(
            resource_type=m["resource_type"],
            resource_id=m["resource_id"],
            resource_name=m["resource_name"],
            score=m["score"],
            distance_km=m["distance_km"],
            availability_status=m["availability_status"],
            match_status="NOTIFIED",
            contact_phone=m.get("contact_phone"),
            address=m.get("address"),
            units_available=m.get("units_available"),
            latitude=m.get("latitude"),
            longitude=m.get("longitude")
        ))

    resp = EmergencyRequestResponse.model_validate(req)
    resp.matches = response_matches
    return resp

@router.get("/", response_model=List[EmergencyRequestResponse])
def list_emergency_requests(
    status: Optional[str] = None,
    blood_group: Optional[str] = None,
    urgency: Optional[str] = None,
    limit: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(EmergencyRequest)
    if status:
        query = query.filter(EmergencyRequest.status == status.upper())
    if blood_group:
        query = query.filter(EmergencyRequest.blood_group == blood_group.upper())
    if urgency:
        query = query.filter(EmergencyRequest.urgency.ilike(urgency))

    requests = query.order_by(EmergencyRequest.created_at.desc()).limit(limit).all()
    results = []
    for r in requests:
        ranked = find_ranked_matches_for_request(db, r)
        res_matches = [
            ResourceMatchItem(
                resource_type=m["resource_type"],
                resource_id=m["resource_id"],
                resource_name=m["resource_name"],
                score=m["score"],
                distance_km=m["distance_km"],
                availability_status=m["availability_status"],
                match_status="NOTIFIED",
                contact_phone=m.get("contact_phone"),
                address=m.get("address"),
                units_available=m.get("units_available"),
                latitude=m.get("latitude"),
                longitude=m.get("longitude")
            ) for m in ranked[:5]
        ]
        item = EmergencyRequestResponse.model_validate(r)
        item.matches = res_matches
        results.append(item)
    return results

@router.get("/{request_code}", response_model=EmergencyRequestResponse)
def get_emergency_request(request_code: str, db: Session = Depends(get_db)):
    req = db.query(EmergencyRequest).filter(EmergencyRequest.request_code == request_code.upper()).first()
    if not req:
        raise HTTPException(status_code=404, detail=f"Request {request_code} not found")

    ranked = find_ranked_matches_for_request(db, req)
    res_matches = [
        ResourceMatchItem(
            resource_type=m["resource_type"],
            resource_id=m["resource_id"],
            resource_name=m["resource_name"],
            score=m["score"],
            distance_km=m["distance_km"],
            availability_status=m["availability_status"],
            match_status="NOTIFIED",
            contact_phone=m.get("contact_phone"),
            address=m.get("address"),
            units_available=m.get("units_available"),
            latitude=m.get("latitude"),
            longitude=m.get("longitude")
        ) for m in ranked
    ]
    resp = EmergencyRequestResponse.model_validate(req)
    resp.matches = res_matches
    return resp

@router.patch("/{request_code}/status", response_model=EmergencyRequestResponse)
async def update_request_status(
    request_code: str,
    payload: StatusUpdateRequest,
    db: Session = Depends(get_db)
):
    req = db.query(EmergencyRequest).filter(EmergencyRequest.request_code == request_code.upper()).first()
    if not req:
        raise HTTPException(status_code=404, detail=f"Request {request_code} not found")

    req.status = payload.status.upper()
    if payload.resource_info:
        req.assigned_resource_info = payload.resource_info
    db.commit()
    db.refresh(req)

    # Broadcast status change event across WebSocket
    event = {
        "event": "STATUS_CHANGED",
        "request_code": req.request_code,
        "new_status": req.status,
        "resource_info": req.assigned_resource_info,
        "timestamp": req.updated_at.isoformat()
    }
    await manager.broadcast(event)

    ranked = find_ranked_matches_for_request(db, req)
    res_matches = [
        ResourceMatchItem(
            resource_type=m["resource_type"],
            resource_id=m["resource_id"],
            resource_name=m["resource_name"],
            score=m["score"],
            distance_km=m["distance_km"],
            availability_status=m["availability_status"],
            match_status="NOTIFIED",
            contact_phone=m.get("contact_phone"),
            address=m.get("address"),
            units_available=m.get("units_available"),
            latitude=m.get("latitude"),
            longitude=m.get("longitude")
        ) for m in ranked
    ]
    resp = EmergencyRequestResponse.model_validate(req)
    resp.matches = res_matches
    return resp
