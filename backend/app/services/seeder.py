from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.user import User, DonorProfile
from app.models.resource import BloodBank, Hospital, Ambulance, Pharmacy
from app.models.inventory import BloodInventory
from app.models.emergency_request import EmergencyRequest, ResourceMatch
from app.utils.security import get_password_hash

def seed_database(db: Session):
    # Check if already seeded
    if db.query(BloodBank).count() > 0:
        return

    print("[INFO] Seeding LifeLink emergency resource network with realistic Bhubaneswar data...")

    # 1. Seed Blood Banks
    banks_data = [
        {
            "name": "Central Red Cross Blood Centre",
            "license_no": "BB-OD-2018-091",
            "category": "Red Cross / Charitable",
            "address": "Unit 9, Near Ram Mandir, Bhubaneswar",
            "city": "Bhubaneswar",
            "latitude": 20.2882,
            "longitude": 85.8365,
            "contact_phone": "+91-674-2391456",
            "operating_hours": "24x7 Emergency",
            "is_verified": True
        },
        {
            "name": "AIIMS Blood Center & Transfusion Medicine",
            "license_no": "BB-OD-2014-042",
            "category": "Govt Apex Institute",
            "address": "Sijua, Patrapada, Bhubaneswar",
            "city": "Bhubaneswar",
            "latitude": 20.2312,
            "longitude": 85.7760,
            "contact_phone": "+91-674-2476789",
            "operating_hours": "24x7 Emergency",
            "is_verified": True
        },
        {
            "name": "Capital Hospital Blood Bank",
            "license_no": "BB-OD-2010-015",
            "category": "Govt District Hospital",
            "address": "Unit 6, Ganga Nagar, Bhubaneswar",
            "city": "Bhubaneswar",
            "latitude": 20.2644,
            "longitude": 85.8202,
            "contact_phone": "+91-674-2391983",
            "operating_hours": "24x7 Emergency",
            "is_verified": True
        },
        {
            "name": "KIMS Hospital Blood Centre",
            "license_no": "BB-OD-2019-118",
            "category": "Private Medical College",
            "address": "KIIT Road, Patia, Bhubaneswar",
            "city": "Bhubaneswar",
            "latitude": 20.3533,
            "longitude": 85.8195,
            "contact_phone": "+91-674-7105300",
            "operating_hours": "24x7 Emergency",
            "is_verified": True
        }
    ]

    blood_banks = []
    for b in banks_data:
        bb = BloodBank(**b)
        db.add(bb)
        blood_banks.append(bb)
    db.commit()

    # 2. Seed Blood Inventories across blood groups and components
    groups = ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"]
    components = ["Packed RBC", "Platelets", "Plasma", "Whole Blood"]
    
    unit_distribution = {
        "O+": 14, "O-": 4, "A+": 18, "A-": 3,
        "B+": 20, "B-": 5, "AB+": 8, "AB-": 2
    }

    for bb in blood_banks:
        for grp in groups:
            for comp in components:
                base_units = unit_distribution.get(grp, 5)
                if comp == "Packed RBC":
                    units = max(1, base_units - (1 if bb.id % 2 == 0 else 0))
                elif comp == "Platelets":
                    units = max(1, base_units // 2)
                elif comp == "Plasma":
                    units = max(2, base_units // 2 + 1)
                else:
                    units = max(0, base_units // 3)

                inv = BloodInventory(
                    blood_bank_id=bb.id,
                    blood_group=grp,
                    component=comp,
                    units_available=units,
                    last_updated=datetime.utcnow() - timedelta(minutes=15 * bb.id)
                )
                db.add(inv)
    db.commit()

    # 3. Seed Hospitals
    hospitals_data = [
        {
            "name": "AIIMS Hospital Bhubaneswar",
            "registration_no": "HOSP-BBSR-01",
            "address": "Sijua, Patrapada, Bhubaneswar",
            "city": "Bhubaneswar",
            "latitude": 20.2312,
            "longitude": 85.7760,
            "emergency_contact": "+91-674-2476000",
            "has_blood_bank": True,
            "total_beds": 960,
            "icu_beds_available": 24
        },
        {
            "name": "Capital Hospital",
            "registration_no": "HOSP-BBSR-02",
            "address": "Unit 6, Bhubaneswar",
            "city": "Bhubaneswar",
            "latitude": 20.2644,
            "longitude": 85.8202,
            "emergency_contact": "+91-674-2391980",
            "has_blood_bank": True,
            "total_beds": 750,
            "icu_beds_available": 12
        },
        {
            "name": "Apollo Hospitals",
            "registration_no": "HOSP-BBSR-03",
            "address": "Plot No. 251, Sainik School Road, Bhubaneswar",
            "city": "Bhubaneswar",
            "latitude": 20.3087,
            "longitude": 85.8336,
            "emergency_contact": "+91-674-6661066",
            "has_blood_bank": False,
            "total_beds": 350,
            "icu_beds_available": 8
        },
        {
            "name": "KIMS Super Specialty Hospital",
            "registration_no": "HOSP-BBSR-04",
            "address": "Kushabhadra Campus 5, Patia, Bhubaneswar",
            "city": "Bhubaneswar",
            "latitude": 20.3533,
            "longitude": 85.8195,
            "emergency_contact": "+91-674-7105000",
            "has_blood_bank": True,
            "total_beds": 500,
            "icu_beds_available": 18
        }
    ]

    for h in hospitals_data:
        db.add(Hospital(**h))
    db.commit()

    # 4. Seed Volunteer Donors
    donors_data = [
        {"name": "Rohan_M", "blood_group": "O+", "lat": 20.2910, "lng": 85.8290, "city": "Bhubaneswar", "radius": 15.0},
        {"name": "Ananya_K", "blood_group": "O-", "lat": 20.2750, "lng": 85.8120, "city": "Bhubaneswar", "radius": 20.0},
        {"name": "Subhash_P", "blood_group": "A+", "lat": 20.3200, "lng": 85.8300, "city": "Bhubaneswar", "radius": 10.0},
        {"name": "Priyanka_D", "blood_group": "B+", "lat": 20.3550, "lng": 85.8180, "city": "Bhubaneswar", "radius": 12.0},
        {"name": "Amit_S", "blood_group": "O+", "lat": 20.2500, "lng": 85.7900, "city": "Bhubaneswar", "radius": 15.0},
        {"name": "Dr_Sneha_R", "blood_group": "AB+", "lat": 20.2980, "lng": 85.8450, "city": "Bhubaneswar", "radius": 10.0}
    ]

    for i, d in enumerate(donors_data):
        user = User(
            name=d["name"],
            email=f"{d['name'].lower()}@example.com",
            phone=f"+91-98765432{10+i}",
            hashed_password=get_password_hash("password123"),
            role="donor",
            is_verified=True
        )
        db.add(user)
        db.flush()

        donor = DonorProfile(
            user_id=user.id,
            display_name=d["name"],
            blood_group=d["blood_group"],
            city=d["city"],
            latitude=d["lat"],
            longitude=d["lng"],
            preferred_radius_km=d["radius"],
            is_available=True,
            emergency_notifications_enabled=True,
            last_donation_date=datetime.utcnow() - timedelta(days=120)
        )
        db.add(donor)
    db.commit()

    # 5. Seed Ambulances
    ambulances_data = [
        {
            "vehicle_number": "OD-02-AX-1081",
            "provider_name": "Govt 108 Emergency Ambulance",
            "ambulance_type": "Advanced Life Support (ALS)",
            "city": "Bhubaneswar",
            "current_latitude": 20.2850,
            "current_longitude": 85.8280,
            "driver_name": "Rajesh Nayak",
            "contact_phone": "+91-9437108108",
            "is_available": True,
            "is_verified": True
        },
        {
            "vehicle_number": "OD-02-BL-3342",
            "provider_name": "Red Cross Emergency Mobile",
            "ambulance_type": "Basic Life Support (BLS)",
            "city": "Bhubaneswar",
            "current_latitude": 20.2990,
            "current_longitude": 85.8350,
            "driver_name": "Bikash Mohanty",
            "contact_phone": "+91-9437209209",
            "is_available": True,
            "is_verified": True
        },
        {
            "vehicle_number": "OD-02-EM-9901",
            "provider_name": "AIIMS Trauma Transport",
            "ambulance_type": "Advanced Life Support (ALS)",
            "city": "Bhubaneswar",
            "current_latitude": 20.2350,
            "current_longitude": 85.7800,
            "driver_name": "Suresh Rout",
            "contact_phone": "+91-9437301301",
            "is_available": True,
            "is_verified": True
        }
    ]

    for amb in ambulances_data:
        db.add(Ambulance(**amb))
    db.commit()

    # 6. Seed Pharmacies
    pharmacies_data = [
        {
            "name": "Apollo 24x7 Pharmacy - Master Canteen",
            "address": "Station Square, Master Canteen, Bhubaneswar",
            "city": "Bhubaneswar",
            "latitude": 20.2680,
            "longitude": 85.8410,
            "contact_phone": "+91-674-2531001",
            "is_24x7": True,
            "is_verified": True,
            "inventory_notes": "Stocked: Emergency Heparin, Tranexamic Acid, Albumin 20%, IV Saline",
            "last_verified_minutes_ago": 6
        },
        {
            "name": "Capital Medicos 24/7",
            "address": "Opposite Capital Hospital Gate 2, Unit 6, Bhubaneswar",
            "city": "Bhubaneswar",
            "latitude": 20.2640,
            "longitude": 85.8190,
            "contact_phone": "+91-674-2395566",
            "is_24x7": True,
            "is_verified": True,
            "inventory_notes": "Stocked: Coagulants, Blood Administration Sets, Cryoprecipitate Filters",
            "last_verified_minutes_ago": 14
        },
        {
            "name": "MedPlus Pharmacy - Patia",
            "address": "Near KIIT Square, Patia, Bhubaneswar",
            "city": "Bhubaneswar",
            "latitude": 20.3540,
            "longitude": 85.8180,
            "contact_phone": "+91-674-2741122",
            "is_24x7": True,
            "is_verified": True,
            "inventory_notes": "Stocked: Emergency adrenaline, Noradrenaline, Plasma expanders",
            "last_verified_minutes_ago": 22
        }
    ]

    for p in pharmacies_data:
        db.add(Pharmacy(**p))
    db.commit()

    # 7. Seed Sample Active Emergency Request (LL-2841)
    req = EmergencyRequest(
        request_code="LL-2841",
        patient_name="Rahul Sharma",
        blood_group="O+",
        component="Packed RBC",
        units_needed=2,
        hospital_name="AIIMS Hospital Bhubaneswar",
        city="Bhubaneswar",
        latitude=20.2312,
        longitude=85.7760,
        urgency="Critical",
        required_within_hours=2.0,
        contact_phone="+91-9876543221",
        additional_notes="Post-accident surgery in ICU-2. Immediate 2 units of Packed RBC required.",
        status="MATCHING"
    )
    db.add(req)
    db.commit()

    print("[SUCCESS] Seeding complete!")
