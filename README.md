# LifeLink — Emergency Resource Coordination Platform

> *"Our problem is not simply finding a blood donor. The problem is coordinating the entire emergency response quickly."*

LifeLink is an end-to-end real-time emergency coordination platform designed to eliminate fragmentation during medical crises. Instead of relying on manual phone calls and disorganized chat groups, LifeLink connects patients, hospitals, verified blood banks, ambulances, and voluntary donors within minutes through an intelligent multi-factor matching engine and live WebSocket dispatch.

---

## 🚀 Key Features

1. **Intelligent Matching & Ranking Engine ("More than CRUD")**:
   - Scores candidate resources from $0\%$ to $99\%$ using a mathematical algorithm combining:
     - **Distance Decay**: Haversine great-circle formula calculating physical distance in kilometers.
     - **Stock Verification**: Live inventory check for exact and compatible blood components (Packed RBC, Platelets, Plasma, Whole Blood).
     - **Urgency Multiplier**: Exponential priority weighting for sub-2-hour critical requests.
     - **Resource Reliability**: Differentiates apex hospitals, blood banks, and verified donors.
     - **Response Probability**: Factored by past donor response rates.

2. **Five-Stage Real-Time Workflow Engine**:
   - Seamlessly tracks requests from creation to delivery:
     $$\text{Matching} \longrightarrow \text{Blood Bank Contacted} \longrightarrow \text{Volunteer Response} \longrightarrow \text{Resource Confirmed} \longrightarrow \text{Completed}$$
   - WebSocket broadcast updates both requester and responder dashboards live without manual page reloads.

3. **Emergency Radar Map (Leaflet / OpenStreetMap)**:
   - Interactive GIS radar plotting:
     - 🩸 **Blood Banks** (Red) with component stock breakdown
     - 🏥 **Apex Hospitals** (Indigo) with ICU bed capacity
     - 🚑 **Ambulance Fleet** (Amber) with BLS/ALS status
     - ❤️ **Volunteer Donors** (Emerald) within preferred radiuses
     - 🆘 **Patient Emergency Beacon** (Pulsing Red) with live distance calculation

4. **Privacy-Preserving Volunteer System**:
   - Protects donor privacy by concealing personal phone numbers from public screens.
   - Ephemeral **Secure Bridge Tokens** facilitate communication only after the donor clicks `[ACCEPT DISPATCH]`.

5. **Hospital & Blood Bank Portals**:
   - Hospital triage center showing active emergency cases and critical counts.
   - e-RaktKosh aligned blood inventory dashboard enabling certified staff to manage units by group and component.

6. **Ambulance & 24x7 Pharmacy Modules**:
   - Fleet tracking with driver verification.
   - Critical medicine search (Heparin, Albumin, Tranexamic Acid) featuring explicit **Telemetry Freshness Timestamps** to avoid misleading guarantees.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+, FastAPI, SQLAlchemy, Pydantic v2, WebSockets, SQLite (zero-config, PostgreSQL-ready).
- **Frontend**: React 19, Vite 8, Tailwind CSS v4, Lucide Icons, Leaflet & React-Leaflet.
- **Geospatial & Math**: Haversine formula, ABO/Rh medical compatibility matrix.

---

## 📁 Project Structure

```
lifelink/
├── backend/
│   ├── app/
│   │   ├── config.py              # Configuration & constants
│   │   ├── database.py            # SQLAlchemy session management
│   │   ├── main.py                # FastAPI entrypoint, CORS & routes
│   │   ├── models/                # Database models (User, Request, Resources, Inventory)
│   │   ├── schemas/               # Pydantic validation schemas
│   │   ├── services/
│   │   │   ├── matching_engine.py # Mathematical ranking algorithm
│   │   │   ├── websocket_manager.py# Real-time WebSocket dispatch hub
│   │   │   └── seeder.py          # Bhubaneswar apex center seed data
│   │   ├── routers/               # REST endpoints for all platform modules
│   │   └── utils/
│   │       ├── geo.py             # Haversine distance calculations
│   │       └── blood_compat.py    # Medical compatibility matrix
│   ├── requirements.txt
│   └── run.py                     # Convenience runner script
├── frontend/
│   ├── src/
│   │   ├── App.jsx                # Root view & live socket integration
│   │   ├── components/            # EmergencyMap, WorkflowTracker, Navbar, Toasts
│   │   ├── pages/                 # Home, CreateRequest, RequestStatus, Portals
│   │   └── services/              # API & WebSocket client connections
│   ├── vite.config.js
│   └── package.json
└── README.md
```

---

## ⚡ How to Run the Project

### 1. Start the Backend API (FastAPI)

Open a terminal in `backend/`:

```powershell
cd C:\Users\kamal\.gemini\antigravity\scratch\lifelink\backend
python run.py
```
- API Server: `http://127.0.0.1:8000`
- Interactive Swagger Docs: `http://127.0.0.1:8000/docs`

> *Note: On initial launch, the backend automatically creates `lifelink.db` and populates realistic medical centers (AIIMS, Capital Hospital, Central Red Cross, active donors, ambulances, pharmacies).*

### 2. Start the Frontend App (React + Vite)

Open a second terminal in `frontend/`:

```powershell
cd C:\Users\kamal\.gemini\antigravity\scratch\lifelink\frontend
npm run dev
```
- Web Application: `http://localhost:3000`

---

## 🎬 Viva Presentation Walkthrough

Follow this 5-minute flow during your presentation:

1. **Homepage (`/`)**: Show the two core calls-to-action: **"I NEED HELP"** vs **"I CAN HELP"**, and explain why emergency response requires unified coordination.
2. **Create Emergency Request**:
   - Submit a request for *Rahul Sharma*, Blood Group *O+*, Component *Packed RBC*, Urgency *Critical* at *AIIMS Hospital Bhubaneswar*.
3. **Inspect the Matching Engine**:
   - View how candidate blood banks and donors are ranked with match percentages (e.g. AIIMS Blood Bank $99\%$, Capital Hospital $94.7\%$, Central Red Cross $92\%$).
   - Point out the medical disclaimer stating that matching scores assist coordination while final compatibility rests with blood bank officers.
4. **Live Volunteer Dispatch**:
   - Switch to the **Volunteer Portal** in a second window.
   - Show the incoming emergency alert, explain the privacy shield (masked phone numbers), and click **[ACCEPT DISPATCH]**.
5. **Real-Time Stepper Transition**:
   - Observe how the requester's workflow stepper moves automatically to **"Volunteer Response"** and displays the assigned coordinator in real-time without reloading.
6. **Emergency Geo-Radar**:
   - Filter between Blood Banks, Hospitals, Ambulances, and Donors on the interactive Leaflet map.
