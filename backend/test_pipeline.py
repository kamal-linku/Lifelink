import sys
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_tests():
    print("--- Starting LifeLink Automated Verification ---")
    
    # 1. Health Check
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("[PASS] 1. Backend health check passed.")

    # 2. Map Resources
    res = client.get("/api/resources/map")
    assert res.status_code == 200
    markers = res.json()
    assert len(markers) >= 10, f"Expected at least 10 map markers, got {len(markers)}"
    print(f"[PASS] 2. Map resources returned {len(markers)} verified medical markers.")

    # 3. Create Emergency Request
    payload = {
        "patient_name": "Test Patient",
        "blood_group": "O+",
        "component": "Packed RBC",
        "units_needed": 2,
        "hospital_name": "AIIMS Hospital Bhubaneswar",
        "city": "Bhubaneswar",
        "latitude": 20.2312,
        "longitude": 85.7760,
        "urgency": "Critical",
        "required_within_hours": 2.0,
        "contact_phone": "+91-9876543221",
        "additional_notes": "Test verification dispatch"
    }
    res = client.post("/api/requests/", json=payload)
    assert res.status_code == 200, f"Create request failed: {res.text}"
    created_req = res.json()
    req_code = created_req["request_code"]
    assert req_code.startswith("LL-")
    assert len(created_req["matches"]) > 0
    top_match = created_req["matches"][0]
    print(f"[PASS] 3. Emergency Request {req_code} created with top match: '{top_match['resource_name']}' (Score: {top_match['score']}%).")

    # 4. Status Update Stepper
    res = client.patch(f"/api/requests/{req_code}/status", json={"status": "CONTACTED"})
    assert res.status_code == 200
    assert res.json()["status"] == "CONTACTED"
    print(f"[PASS] 4. Workflow stepper updated status to CONTACTED.")

    # 5. Volunteer Accept Response
    res = client.post(f"/api/volunteers/1/respond?request_code={req_code}&action=ACCEPT")
    assert res.status_code == 200
    resp_data = res.json()
    assert resp_data["status"] == "ACCEPTED"
    assert "secure_token" in resp_data
    print(f"[PASS] 5. Volunteer accepted dispatch. Masked bridge token issued: {resp_data['secure_token']}")

    # 6. Verify Request Status after Volunteer Acceptance
    res = client.get(f"/api/requests/{req_code}")
    assert res.status_code == 200
    assert res.json()["status"] == "RESPONDED"
    print(f"[PASS] 6. Request status transitioned automatically to RESPONDED.")

    # 7. Hospital Dashboard
    res = client.get("/api/hospital/dashboard")
    assert res.status_code == 200
    dash = res.json()
    assert "metrics" in dash
    assert dash["metrics"]["active_requests"] >= 1
    print(f"[PASS] 7. Hospital dashboard active requests count: {dash['metrics']['active_requests']}.")

    print("--- ALL 7 LIFELINK SYSTEM TESTS PASSED SUCCESSFULLY! ---")

if __name__ == "__main__":
    run_tests()
