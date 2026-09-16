from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.resource import BloodBank, Hospital
from app.models.inventory import BloodInventory
from app.models.user import DonorProfile
from app.models.emergency_request import EmergencyRequest
from app.utils.geo import haversine_distance
from app.utils.blood_compat import is_blood_compatible, get_compatible_donor_groups

def calculate_match_score(
    distance_km: float,
    is_available: bool,
    resource_type: str,
    urgency: str,
    units_needed: int,
    units_available: int = 0,
    is_exact_group: bool = True
) -> float:
    """
    Intelligent Multi-factor Emergency Ranking Algorithm.
    Weights:
      - Availability & Stock (35%)
      - Distance Decay (30%)
      - Resource Reliability Type (15%)
      - Urgency & Time Sensitivity (10%)
      - Compatibility match (10%)
    """
    # 1. Availability Score (0 to 35)
    if resource_type == "blood_bank":
        if units_available >= units_needed:
            avail_score = 35.0
        elif units_available > 0:
            avail_score = 25.0 * (units_available / units_needed)
        else:
            avail_score = 5.0
    elif resource_type == "volunteer":
        avail_score = 30.0 if is_available else 5.0
    else:
        avail_score = 25.0

    # 2. Distance Decay Score (0 to 30)
    # Beyond 25km, score drops exponentially; within 5km, top score
    max_radius = 25.0
    if distance_km <= 2.0:
        dist_score = 30.0
    elif distance_km <= max_radius:
        dist_score = 30.0 * (1.0 - (distance_km / max_radius) * 0.75)
    else:
        dist_score = max(2.0, 30.0 * (max_radius / distance_km))

    # 3. Resource Reliability Type Score (0 to 15)
    # Verified blood bank institutions rank highest for immediate confirmed release
    if resource_type == "blood_bank":
        type_score = 15.0
    elif resource_type == "hospital":
        type_score = 14.0
    elif resource_type == "volunteer":
        type_score = 12.0
    else:
        type_score = 10.0

    # 4. Urgency Weight (0 to 10)
    # If Critical and within close proximity, boost urgency score
    urgency_lower = urgency.lower()
    if urgency_lower == "critical":
        urgency_score = 10.0 if distance_km < 10.0 else 7.0
    elif urgency_lower == "urgent":
        urgency_score = 8.0
    else:
        urgency_score = 5.0

    # 5. Exact vs Compatible Group Score (0 to 10)
    group_score = 10.0 if is_exact_group else 7.0

    total_score = avail_score + dist_score + type_score + urgency_score + group_score
    # Cap between 15% and 99%
    final_score = min(99.0, max(15.0, total_score))
    return round(final_score, 1)

def find_ranked_matches_for_request(db: Session, request: EmergencyRequest) -> List[Dict[str, Any]]:
    """
    Search across Blood Banks and Registered Volunteers,
    compute compatibility and match score, and return prioritized resources.
    """
    matches = []
    compatible_groups = get_compatible_donor_groups(request.blood_group, request.component)

    # 1. Search Blood Banks & their Inventory
    blood_banks = db.query(BloodBank).filter(BloodBank.is_verified == True).all()
    for bank in blood_banks:
        dist = haversine_distance(request.latitude, request.longitude, bank.latitude, bank.longitude)
        
        # Check stock for requested component & compatible groups
        inventories = db.query(BloodInventory).filter(
            BloodInventory.blood_bank_id == bank.id,
            BloodInventory.component == request.component,
            BloodInventory.blood_group.in_(compatible_groups)
        ).all()

        total_units = sum(inv.units_available for inv in inventories)
        exact_inv = next((inv for inv in inventories if inv.blood_group == request.blood_group), None)
        exact_units = exact_inv.units_available if exact_inv else 0

        is_exact = exact_units > 0
        has_stock = total_units > 0

        score = calculate_match_score(
            distance_km=dist,
            is_available=has_stock,
            resource_type="blood_bank",
            urgency=request.urgency,
            units_needed=request.units_needed,
            units_available=total_units,
            is_exact_group=is_exact
        )

        matches.append({
            "resource_type": "blood_bank",
            "resource_id": bank.id,
            "resource_name": bank.name,
            "category": bank.category,
            "blood_group": request.blood_group if is_exact else (inventories[0].blood_group if inventories else request.blood_group),
            "units_available": total_units,
            "distance_km": dist,
            "score": score,
            "availability_status": "CONFIRMED" if total_units >= request.units_needed else ("LIMITED" if total_units > 0 else "NO_STOCK"),
            "contact_phone": bank.contact_phone,
            "address": bank.address,
            "latitude": bank.latitude,
            "longitude": bank.longitude,
            "operating_hours": bank.operating_hours
        })

    # 2. Search Registered Volunteers / Donors
    donors = db.query(DonorProfile).filter(
        DonorProfile.is_available == True,
        DonorProfile.blood_group.in_(compatible_groups)
    ).all()

    for donor in donors:
        dist = haversine_distance(request.latitude, request.longitude, donor.latitude, donor.longitude)
        # Check if within preferred radius (or default 15km)
        if dist <= max(donor.preferred_radius_km, 15.0):
            is_exact = donor.blood_group == request.blood_group
            score = calculate_match_score(
                distance_km=dist,
                is_available=True,
                resource_type="volunteer",
                urgency=request.urgency,
                units_needed=request.units_needed,
                units_available=1,
                is_exact_group=is_exact
            )

            matches.append({
                "resource_type": "volunteer",
                "resource_id": donor.id,
                "resource_name": f"Verified Donor ({donor.display_name})",
                "category": "Volunteer Donor",
                "blood_group": donor.blood_group,
                "units_available": 1,
                "distance_km": dist,
                "score": score,
                "availability_status": "AVAILABLE",
                "contact_phone": "SECURE_MASKED_CONTACT", # Never expose raw phone number publicly!
                "address": f"{donor.city} (Within {round(dist, 1)} km)",
                "latitude": donor.latitude,
                "longitude": donor.longitude,
                "operating_hours": "Ready to Respond"
            })

    # 3. Sort prioritized results descending by score
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches
