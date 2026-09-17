import React, { useState, useEffect } from "react";
import { 
  Heart, Shield, Bell, CheckCircle2, XCircle, 
  MapPin, Phone, Lock, Sparkles, AlertTriangle 
} from "lucide-react";
import { api } from "../services/api";

export function VolunteerPortal({ onAcceptSuccess }) {
  const [volunteers, setVolunteers] = useState([]);
  const [activeDonorId, setActiveDonorId] = useState(1);
  const [isAvailable, setIsAvailable] = useState(true);
  const [preferredRadius, setPreferredRadius] = useState(10);
  const [incomingAlerts, setIncomingAlerts] = useState([]);
  const [acceptedBridge, setAcceptedBridge] = useState(null);

  // New registration form state
  const [registerForm, setRegisterForm] = useState({
    display_name: "Aman_B",
    blood_group: "O+",
    city: "Bhubaneswar",
    preferred_radius_km: 15,
    phone: "+91-9876543299",
    email: "aman@example.com",
    latitude: 20.2961,
    longitude: 85.8245,
    is_available: true,
    emergency_notifications_enabled: true
  });
  const [regSuccess, setRegSuccess] = useState(false);

  useEffect(() => {
    loadVolunteers();
    loadEmergencyAlerts();
  }, []);

  const loadVolunteers = async () => {
    try {
      const list = await api.getVolunteers();
      setVolunteers(list);
      if (list.length > 0 && !activeDonorId) {
        setActiveDonorId(list[0].id);
        setIsAvailable(list[0].is_available);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const loadEmergencyAlerts = async () => {
    try {
      const reqs = await api.listRequests({ status: "MATCHING" });
      setIncomingAlerts(reqs);
    } catch (err) {
      console.error(err);
    }
  };

  const handleToggleAvailability = async () => {
    const nextState = !isAvailable;
    setIsAvailable(nextState);
    if (activeDonorId) {
      await api.toggleVolunteerAvailability(activeDonorId, nextState);
    }
  };

  const handleRespond = async (requestCode, action) => {
    try {
      const res = await api.volunteerRespond(activeDonorId, requestCode, action);
      if (action === "ACCEPT") {
        setAcceptedBridge(res);
        setIncomingAlerts((prev) => prev.filter((a) => a.request_code !== requestCode));
        if (onAcceptSuccess) onAcceptSuccess(requestCode);
      } else {
        setIncomingAlerts((prev) => prev.filter((a) => a.request_code !== requestCode));
      }
    } catch (err) {
      alert(err.message);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const created = await api.registerVolunteer(registerForm);
      setRegSuccess(true);
      await loadVolunteers();
      setActiveDonorId(created.id);
    } catch (err) {
      alert("Registration error: " + err.message);
    }
  };

  const activeDonor = volunteers.find((v) => v.id === activeDonorId) || volunteers[0];

  return (
    <div className="max-w-5xl mx-auto space-y-10 pb-16">
      {/* Header Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center space-x-2 bg-emerald-500/10 border border-emerald-500/30 px-3 py-1 rounded-full text-xs font-bold text-emerald-400 mb-2">
              <Heart className="w-4 h-4 text-emerald-400 fill-current" />
              <span>LifeLink Voluntary Donor Network</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-black text-white">Volunteer Coordination Portal</h2>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Privacy-preserving emergency dispatch. Your direct phone number is never shown publicly.
            </p>
          </div>

          {/* Quick Identity Switcher (for Viva Presentation) */}
          <div className="bg-slate-800/80 p-2.5 rounded-2xl border border-slate-700 flex items-center space-x-2">
            <span className="text-xs text-slate-400 font-semibold pl-2">Active Profile:</span>
            <select
              value={activeDonorId}
              onChange={(e) => {
                const id = parseInt(e.target.value);
                setActiveDonorId(id);
                const d = volunteers.find((v) => v.id === id);
                if (d) setIsAvailable(d.is_available);
              }}
              className="bg-slate-900 text-white text-xs font-bold rounded-xl px-3 py-1.5 border border-slate-600 focus:outline-none focus:border-rose-500"
            >
              {volunteers.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.display_name} ({d.blood_group})
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Main Grid: Profile Settings & Live Dispatch Queue */}
      <div className="grid md:grid-cols-12 gap-8">
        {/* Left Column: Volunteer Profile Settings */}
        <div className="md:col-span-5 space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-6">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <span className="text-xs uppercase font-bold text-slate-400">Profile</span>
                <h4 className="text-lg font-black text-white">{activeDonor?.display_name || "Volunteer"}</h4>
              </div>
              <span className="text-sm font-black bg-rose-500/20 text-rose-400 px-3 py-1 rounded-xl border border-rose-500/30">
                {activeDonor?.blood_group || "O+"}
              </span>
            </div>

            {/* Availability Toggle */}
            <div className="flex items-center justify-between p-4 rounded-2xl bg-slate-800/60 border border-slate-700">
              <div>
                <h5 className="text-sm font-bold text-white">Emergency Availability</h5>
                <p className="text-xs text-slate-400">Receive real-time match alerts</p>
              </div>
              <button
                onClick={handleToggleAvailability}
                className={`w-14 h-8 flex items-center rounded-full p-1 transition-colors ${
                  isAvailable ? "bg-emerald-500" : "bg-slate-700"
                }`}
              >
                <div
                  className={`bg-white w-6 h-6 rounded-full shadow-md transform transition-transform ${
                    isAvailable ? "translate-x-6" : "translate-x-0"
                  }`}
                />
              </button>
            </div>

            {/* Preferred Radius Slider */}
            <div className="space-y-2 p-4 rounded-2xl bg-slate-800/60 border border-slate-700">
              <div className="flex justify-between text-xs font-semibold">
                <span className="text-slate-300">Dispatch Radius</span>
                <span className="text-emerald-400 font-bold">{preferredRadius} km</span>
              </div>
              <input
                type="range"
                min="2"
                max="30"
                value={preferredRadius}
                onChange={(e) => setPreferredRadius(parseInt(e.target.value))}
                className="w-full accent-emerald-500 cursor-pointer"
              />
              <p className="text-[10px] text-slate-400">Alert me only for hospitals and patients within this zone</p>
            </div>

            {/* Privacy Guarantee Card */}
            <div className="p-4 rounded-2xl bg-slate-800/40 border border-slate-700/60 space-y-2">
              <div className="flex items-center space-x-2 text-indigo-400 text-xs font-bold">
                <Lock className="w-4 h-4" />
                <span>Zero Phone Leakage Guarantee</span>
              </div>
              <p className="text-[11px] text-slate-400 leading-relaxed">
                LifeLink issues ephemeral secure bridge tokens when you click Accept. Your actual phone number and personal identity remain shielded.
              </p>
            </div>
          </div>
        </div>

        {/* Right Column: Incoming Real-Time Emergency Alerts */}
        <div className="md:col-span-7 space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 rounded-full bg-rose-500 animate-ping" />
                <h3 className="text-base font-black text-white">Emergency Dispatches Near You</h3>
              </div>
              <span className="text-xs bg-slate-800 text-slate-300 px-2.5 py-1 rounded-lg">
                {incomingAlerts.length} Waiting
              </span>
            </div>

            {acceptedBridge && (
              <div className="p-5 rounded-2xl bg-emerald-950/60 border border-emerald-500/80 shadow-lg text-white space-y-3 animate-fade-in">
                <div className="flex items-center space-x-2 text-emerald-400 font-bold text-sm">
                  <CheckCircle2 className="w-5 h-5" />
                  <span>Response Registered! Thank You!</span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  The hospital coordinator has been notified that you are responding. You can connect securely via the emergency bridge:
                </p>
                <div className="bg-slate-900 p-3 rounded-xl border border-emerald-500/40 font-mono text-xs text-emerald-300">
                  {acceptedBridge.secure_token}
                </div>
              </div>
            )}

            {incomingAlerts.length === 0 && !acceptedBridge ? (
              <div className="py-12 text-center text-slate-500 space-y-2">
                <Shield className="w-8 h-8 mx-auto text-slate-600" />
                <p className="text-xs font-semibold">No critical requests currently waiting in your area.</p>
                <p className="text-[10px] text-slate-600">You will hear an instant alert when a matching patient needs help.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {incomingAlerts.map((alert) => (
                  <div
                    key={alert.request_code}
                    className="p-5 rounded-2xl bg-slate-850 border border-rose-500/40 shadow-lg shadow-rose-950/20 space-y-3"
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="flex items-center space-x-2">
                          <span className="font-mono text-xs font-bold text-rose-400 bg-rose-500/20 px-2 py-0.5 rounded">
                            {alert.request_code}
                          </span>
                          <span className="text-xs font-bold text-red-400 uppercase">
                            {alert.urgency}
                          </span>
                        </div>
                        <h4 className="font-bold text-base text-white mt-1">
                          Patient: {alert.patient_name}
                        </h4>
                        <p className="text-xs text-slate-400">{alert.hospital_name}, {alert.city}</p>
                      </div>

                      <div className="text-right">
                        <span className="text-sm font-black text-rose-400">
                          {alert.units_needed} Units
                        </span>
                        <span className="block text-[10px] text-slate-400">
                          {alert.blood_group} ({alert.component})
                        </span>
                      </div>
                    </div>

                    <div className="bg-slate-900/60 p-3 rounded-xl text-xs text-slate-300">
                      <strong>Notes:</strong> {alert.additional_notes || "Urgent emergency requirement."}
                    </div>

                    {/* ACCEPT / DECLINE BUTTONS (From Specification Page 8) */}
                    <div className="grid grid-cols-2 gap-3 pt-2">
                      <button
                        onClick={() => handleRespond(alert.request_code, "ACCEPT")}
                        className="py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-black text-xs flex items-center justify-center space-x-1.5 shadow-lg shadow-emerald-600/30 transition-colors"
                      >
                        <CheckCircle2 className="w-4 h-4" />
                        <span>ACCEPT DISPATCH</span>
                      </button>

                      <button
                        onClick={() => handleRespond(alert.request_code, "DECLINE")}
                        className="py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 font-bold text-xs flex items-center justify-center space-x-1.5 transition-colors"
                      >
                        <XCircle className="w-4 h-4" />
                        <span>DECLINE</span>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
