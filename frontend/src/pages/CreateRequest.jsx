import React, { useState } from "react";
import { AlertOctagon, Droplet, Clock, Hospital, Phone, FileText, Send, Sparkles } from "lucide-react";
import { api } from "../services/api";

export function CreateRequest({ onRequestCreated }) {
  const [formData, setFormData] = useState({
    patient_name: "Rahul Sharma",
    blood_group: "O+",
    component: "Packed RBC",
    units_needed: 2,
    hospital_name: "AIIMS Hospital Bhubaneswar",
    city: "Bhubaneswar",
    latitude: 20.2312,
    longitude: 85.7760,
    urgency: "Critical",
    required_within_hours: 2.0,
    contact_phone: "+91-9876543221",
    additional_notes: "Emergency trauma operation scheduled. Immediate units needed.",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const hospitalsList = [
    { name: "AIIMS Hospital Bhubaneswar", lat: 20.2312, lng: 85.7760 },
    { name: "Capital Hospital Bhubaneswar", lat: 20.2644, lng: 85.8202 },
    { name: "Apollo Hospitals Bhubaneswar", lat: 20.3087, lng: 85.8336 },
    { name: "KIMS Super Specialty Hospital", lat: 20.3533, lng: 85.8195 },
  ];

  const handleHospitalChange = (e) => {
    const selected = hospitalsList.find((h) => h.name === e.target.value);
    if (selected) {
      setFormData({
        ...formData,
        hospital_name: selected.name,
        latitude: selected.lat,
        longitude: selected.lng,
      });
    } else {
      setFormData({ ...formData, hospital_name: e.target.value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const created = await api.createRequest(formData);
      onRequestCreated(created.request_code);
    } catch (err) {
      setError(err.message || "Failed to create emergency request");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto pb-16">
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-10 shadow-2xl">
        {/* Header */}
        <div className="border-b border-slate-800 pb-6 mb-8">
          <div className="inline-flex items-center space-x-2 bg-rose-500/10 border border-rose-500/30 px-3 py-1 rounded-full text-xs font-bold text-rose-400 mb-3">
            <AlertOctagon className="w-4 h-4 text-rose-500 animate-pulse" />
            <span>Emergency Dispatch Trigger</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-black text-white">Create Emergency Request</h2>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            LifeLink Matching Engine will scan nearby blood banks, hospitals, and voluntary donors within milliseconds.
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-xl bg-rose-950/60 border border-rose-500 text-rose-200 text-xs font-semibold">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Patient Details */}
          <div className="space-y-4">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">1. Patient Details</h4>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Patient Full Name</label>
              <input
                type="text"
                required
                value={formData.patient_name}
                onChange={(e) => setFormData({ ...formData, patient_name: e.target.value })}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-rose-500"
                placeholder="e.g. Rahul Sharma"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Blood Group</label>
                <select
                  value={formData.blood_group}
                  onChange={(e) => setFormData({ ...formData, blood_group: e.target.value })}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-rose-500 font-bold"
                >
                  {["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"].map((bg) => (
                    <option key={bg} value={bg}>{bg}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Component Needed</label>
                <select
                  value={formData.component}
                  onChange={(e) => setFormData({ ...formData, component: e.target.value })}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-rose-500"
                >
                  <option value="Packed RBC">Packed RBC</option>
                  <option value="Platelets">Platelets</option>
                  <option value="Plasma">Plasma</option>
                  <option value="Whole Blood">Whole Blood</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Units Required</label>
                <input
                  type="number"
                  min="1"
                  max="10"
                  required
                  value={formData.units_needed}
                  onChange={(e) => setFormData({ ...formData, units_needed: parseInt(e.target.value) || 1 })}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-rose-500 font-bold"
                />
              </div>
            </div>
          </div>

          {/* Location & Hospital */}
          <div className="space-y-4 pt-4 border-t border-slate-800">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">2. Hospital & Location</h4>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Hospital / Medical Center</label>
              <select
                value={formData.hospital_name}
                onChange={handleHospitalChange}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-rose-500"
              >
                {hospitalsList.map((h) => (
                  <option key={h.name} value={h.name}>{h.name}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Urgency & Timeline */}
          <div className="space-y-4 pt-4 border-t border-slate-800">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">3. Urgency & Timeframe</h4>
            <div className="grid sm:grid-cols-3 gap-3">
              {[
                { id: "Normal", desc: "Within 24 hours", color: "border-slate-700 hover:border-slate-600" },
                { id: "Urgent", desc: "Within 6-12 hours", color: "border-amber-500/50 text-amber-300" },
                { id: "Critical", desc: "Immediate (Under 2 hrs)", color: "border-rose-500 bg-rose-500/10 text-rose-300 ring-2 ring-rose-500/20" },
              ].map((lvl) => (
                <label
                  key={lvl.id}
                  className={`flex flex-col p-3 rounded-xl border cursor-pointer transition-all ${
                    formData.urgency === lvl.id
                      ? "border-rose-500 bg-rose-500/20 text-white font-bold"
                      : "border-slate-800 bg-slate-800/40 text-slate-400 hover:bg-slate-800"
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <input
                      type="radio"
                      name="urgency"
                      value={lvl.id}
                      checked={formData.urgency === lvl.id}
                      onChange={(e) => setFormData({ ...formData, urgency: e.target.value })}
                      className="accent-rose-500"
                    />
                    <span className="text-sm font-black">{lvl.id}</span>
                  </div>
                  <span className="text-[11px] text-slate-400 mt-1">{lvl.desc}</span>
                </label>
              ))}
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Required Within (Hours)</label>
                <input
                  type="number"
                  step="0.5"
                  min="0.5"
                  value={formData.required_within_hours}
                  onChange={(e) => setFormData({ ...formData, required_within_hours: parseFloat(e.target.value) || 2 })}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-rose-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Emergency Attendant Contact Phone</label>
                <input
                  type="tel"
                  required
                  value={formData.contact_phone}
                  onChange={(e) => setFormData({ ...formData, contact_phone: e.target.value })}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-rose-500"
                  placeholder="+91-9876543221"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Additional Information / Ward / ICU No.</label>
              <textarea
                rows="2"
                value={formData.additional_notes}
                onChange={(e) => setFormData({ ...formData, additional_notes: e.target.value })}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-rose-500"
                placeholder="Doctor prescription details or specific bed location"
              />
            </div>
          </div>

          {/* Submit Action */}
          <div className="pt-4">
            <button
              type="submit"
              disabled={loading}
              className="w-full py-4 rounded-2xl bg-gradient-to-r from-rose-600 to-red-600 hover:from-rose-500 hover:to-red-500 text-white font-black text-base shadow-xl shadow-rose-600/40 border border-rose-400/30 flex items-center justify-center space-x-2 group transition-all"
            >
              <AlertOctagon className="w-5 h-5 group-hover:animate-spin" />
              <span>{loading ? "INITIALIZING MATCHING ENGINE..." : "CREATE EMERGENCY REQUEST"}</span>
            </button>
            <p className="text-[11px] text-center text-slate-400 mt-2">
              All nearby blood banks and registered voluntary donors within radius will be alerted immediately.
            </p>
          </div>
        </form>
      </div>
    </div>
  );
}
