from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.emergency_request import EmergencyRequest
from app.models.inventory import BloodInventory
from app.models.resource import BloodBank, Hospital, Ambulance
from app.services.websocket_manager import manager

router = APIRouter(prefix="/api/hospital", tags=["Hospital & Blood Bank Dashboard"])

class InventoryUpdateRequest(BaseModel):
    blood_bank_id: int
    blood_group: str
    component: str
    units_delta: int # e.g. +2 or -1

@router.get("/dashboard")
def get_hospital_dashboard_metrics(db: Session = Depends(get_db)):
    active_requests = db.query(EmergencyRequest).filter(
        EmergencyRequest.status.in_(["MATCHING", "CONTACTED", "RESPONDED", "CONFIRMED"])
    ).all()
    
    critical_count = sum(1 for r in active_requests if r.urgency.lower() == "critical")
    blood_requests_count = len(active_requests)
    ambulance_count = db.query(Ambulance).filter(Ambulance.is_available == True).count()

    total_requests_all = db.query(EmergencyRequest).count()
    completed_count = db.query(EmergencyRequest).filter(EmergencyRequest.status == "COMPLETED").count()

    # Total units in inventory
    inventories = db.query(BloodInventory).all()
    stock_summary = {}
    for inv in inventories:
        key = inv.blood_group
        stock_summary[key] = stock_summary.get(key, 0) + inv.units_available

    return {
        "metrics": {
            "active_requests": len(active_requests),
            "critical_cases": critical_count,
            "blood_requests": blood_requests_count,
            "ambulances_available": ambulance_count
        },
        "todays_activity": {
            "requests_received": total_requests_all,
            "resolved": completed_count,
            "pending": len(active_requests)
        },
        "inventory_by_group": stock_summary,
        "recent_requests": [
            {
                "request_code": r.request_code,
                "patient": r.patient_name,
                "blood_group": r.blood_group,
                "units": r.units_needed,
                "hospital": r.hospital_name,
                "urgency": r.urgency,
                "status": r.status,
                "time": r.created_at.strftime("%H:%M:%S")
            } for r in active_requests[:6]
        ]
    }

@router.post("/inventory/update")
async def update_blood_inventory(payload: InventoryUpdateRequest, db: Session = Depends(get_db)):
    inv = db.query(BloodInventory).filter(
        BloodInventory.blood_bank_id == payload.blood_bank_id,
        BloodInventory.blood_group == payload.blood_group.upper(),
        BloodInventory.component == payload.component
    ).first()

    if not inv:
        # Create if missing
        inv = BloodInventory(
            blood_bank_id=payload.blood_bank_id,
            blood_group=payload.blood_group.upper(),
            component=payload.component,
            units_available=max(0, payload.units_delta)
        )
        db.add(inv)
    else:
        inv.units_available = max(0, inv.units_available + payload.units_delta)
        inv.last_updated = datetime.utcnow()

    db.commit()
    db.refresh(inv)

    bank = db.query(BloodBank).filter(BloodBank.id == payload.blood_bank_id).first()
    bank_name = bank.name if bank else "Blood Centre"

    # WS Notification
    await manager.broadcast({
        "event": "INVENTORY_UPDATED",
        "blood_bank_name": bank_name,
        "blood_group": inv.blood_group,
        "component": inv.component,
        "new_units": inv.units_available
    })

    return {
        "success": True,
        "blood_bank_id": payload.blood_bank_id,
        "blood_group": inv.blood_group,
        "component": inv.component,
        "units_available": inv.units_available
    }
