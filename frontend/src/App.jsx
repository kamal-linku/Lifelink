import React, { useState, useEffect } from "react";
import { Navbar } from "./components/Navbar";
import { LiveNotificationToast } from "./components/LiveNotificationToast";
import { EmergencyMap } from "./components/EmergencyMap";
import { Home } from "./pages/Home";
import { CreateRequest } from "./pages/CreateRequest";
import { RequestStatus } from "./pages/RequestStatus";
import { VolunteerPortal } from "./pages/VolunteerPortal";
import { HospitalPortal } from "./pages/HospitalPortal";
import { BloodBankPortal } from "./pages/BloodBankPortal";
import { AmbulanceDirectory } from "./pages/AmbulanceDirectory";
import { PharmacyDirectory } from "./pages/PharmacyDirectory";
import { EmergencySocket } from "./services/websocket";

export function App() {
  const [currentTab, setCurrentTab] = useState("home");
  const [activeRequestCode, setActiveRequestCode] = useState("LL-2841");
  const [liveToast, setLiveToast] = useState(null);

  useEffect(() => {
    // Connect to WebSocket dispatcher
    const socket = new EmergencySocket("requesters");
    const unsubscribe = socket.subscribe((eventData) => {
      console.log("[WebSocket Event Received]", eventData);
      if (
        eventData.event === "EMERGENCY_CREATED" ||
        eventData.event === "VOLUNTEER_ACCEPTED" ||
        eventData.event === "STATUS_CHANGED"
      ) {
        setLiveToast(eventData);
      }
    });

    return () => {
      unsubscribe();
      socket.close();
    };
  }, []);

  const handleRequestCreated = (newCode) => {
    setActiveRequestCode(newCode);
    setCurrentTab("status");
  };

  const handleSelectRequest = (code) => {
    setActiveRequestCode(code);
    setCurrentTab("status");
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-rose-500 selection:text-white">
      {/* Top Navigation */}
      <Navbar currentTab={currentTab} setCurrentTab={setCurrentTab} />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-8">
        {currentTab === "home" && (
          <Home
            onNavigate={(tab) => setCurrentTab(tab)}
            onSelectRequest={handleSelectRequest}
          />
        )}

        {currentTab === "create-request" && (
          <CreateRequest onRequestCreated={handleRequestCreated} />
        )}

        {currentTab === "status" && (
          <RequestStatus
            requestCode={activeRequestCode}
            onBack={() => setCurrentTab("home")}
          />
        )}

        {currentTab === "map" && (
          <div className="space-y-6 pb-16">
            <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl">
              <h2 className="text-2xl font-black text-white">Full-Screen Emergency Geo-Radar</h2>
              <p className="text-xs text-slate-400 mt-1">
                Real-time geospatial coordinate mapping for hospitals, blood banks, ambulances, and active volunteer donors.
              </p>
            </div>
            <EmergencyMap />
          </div>
        )}

        {currentTab === "volunteer" && (
          <VolunteerPortal
            onAcceptSuccess={(code) => {
              setActiveRequestCode(code);
              setCurrentTab("status");
            }}
          />
        )}

        {currentTab === "hospital" && (
          <HospitalPortal onSelectRequest={handleSelectRequest} />
        )}

        {currentTab === "blood-bank" && <BloodBankPortal />}

        {currentTab === "ambulances" && <AmbulanceDirectory />}

        {currentTab === "pharmacies" && <PharmacyDirectory />}
      </main>

      {/* Live Floating WebSocket Notification Toast */}
      {liveToast && (
        <LiveNotificationToast
          notification={liveToast}
          onClose={() => setLiveToast(null)}
          onAction={() => {
            if (liveToast.request_code) {
              setActiveRequestCode(liveToast.request_code);
              setCurrentTab("status");
            }
            setLiveToast(null);
          }}
        />
      )}

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-8 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 space-y-2">
          <p className="font-semibold text-slate-400">
            LifeLink &bull; Intelligent Emergency Resource Coordination Platform
          </p>
          <p className="text-[11px] text-slate-600">
            Designed for real-time emergency triage and multi-resource synchronization. Medical suitability determined by certified blood banks.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
