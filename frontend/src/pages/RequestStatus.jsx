import React, { useEffect, useState } from "react";
import { 
  AlertOctagon, Phone, Navigation, CheckCircle2, 
  Clock, ShieldAlert, Sparkles, RefreshCw, Info, ExternalLink 
} from "lucide-react";
import { api } from "../services/api";
import { WorkflowTracker } from "../components/WorkflowTracker";
import { EmergencyMap } from "../components/EmergencyMap";

export function RequestStatus({ requestCode, onBack }) {
  const [request, setRequest] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchRequestDetails = async () => {
    try {
      const data = await api.getRequest(requestCode);
      setRequest(data);
    } catch (err) {
      setError(err.message || "Failed to fetch request details");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRequestDetails();
    // Auto polling interval as backup to WebSocket
    const interval = setInterval(fetchRequestDetails, 5000);
    return () => clearInterval(interval);
  }, [requestCode]);

  const handleStatusUpdate = async (newStatus) => {
    try {
      const updated = await api.updateRequestStatus(requestCode, newStatus);
      setRequest(updated);
    } catch (err) {
      console.error("Failed to update status", err);
    }
  };

  if (loading && !request) {
    return (
      <div className="py-24 text-center text-slate-400 space-y-4">
        <RefreshCw className="w-8 h-8 mx-auto animate-spin text-rose-500" />
        <p className="text-sm font-semibold">Scanning resources and calculating match scores...</p>
      </div>
    );
  }

  if (error || !request) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center">
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8">
          <AlertOctagon className="w-12 h-12 text-rose-500 mx-auto mb-4" />
          <h3 className="text-xl font-bold text-white">Emergency Request Not Found</h3>
          <p className="text-xs text-slate-400 mt-2">{error || "Could not retrieve request details."}</p>
          <button
            onClick={onBack}
            className="mt-6 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-bold"
          >
            &larr; Back to Safety Hub
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 pb-16">
      {/* Top Banner with Request Code & Patient Info */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center space-x-3">
              <span className="bg-rose-500/10 text-rose-400 font-mono text-xs font-black px-3 py-1 rounded-lg border border-rose-500/20">
                REQUEST #{request.request_code}
              </span>
              <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full uppercase ${
                request.urgency.toLowerCase() === "critical"
                  ? "bg-red-500/20 text-red-400 border border-red-500/30"
                  : "bg-amber-500/20 text-amber-400"
              }`}>
                {request.urgency}
              </span>
            </div>

            <h1 className="text-2xl sm:text-3xl font-black text-white mt-2">
              {request.patient_name} &bull; {request.blood_group} ({request.component})
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              {request.hospital_name}, {request.city} &bull; Required within {request.required_within_hours} Hours
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={fetchRequestDetails}
              className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
              title="Refresh matches"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
            <div className="bg-rose-600 text-white px-4 py-2 rounded-xl text-xs font-black shadow-lg shadow-rose-600/30">
              {request.units_needed} UNITS NEEDED
            </div>
          </div>
        </div>

        {/* Workflow Pipeline Engine */}
        <div className="mt-6">
          <WorkflowTracker
            currentStatus={request.status}
            assignedResource={request.assigned_resource_info}
            onRequestStatusUpdate={handleStatusUpdate}
          />
        </div>
      </div>

      {/* Mandatory Medical Disclaimer Banner */}
      <div className="bg-amber-950/30 border border-amber-500/30 rounded-2xl p-4 flex items-start space-x-3 text-amber-300 text-xs">
        <Info className="w-5 h-5 flex-shrink-0 mt-0.5 text-amber-400" />
        <div>
          <strong className="font-bold">Important Medical Protocol:</strong> LifeLink calculates an emergency resource ranking score based on location proximity and reported stock. Blood compatibility verification, screening, and transfusion release remain solely under the authority of licensed medical officers.
        </div>
      </div>

      {/* Main Grid: Ranked Matches + Live Radar Map */}
      <div className="grid lg:grid-cols-12 gap-8">
        {/* Left Column: Top Prioritized Matches (Engine Output) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-black text-white flex items-center space-x-2">
                <span>Matching Engine Results</span>
                <span className="bg-rose-500/20 text-rose-400 text-[10px] font-bold px-2 py-0.5 rounded-full border border-rose-500/30">
                  {request.matches?.length || 0} Ranked
                </span>
              </h3>
              <p className="text-xs text-slate-400">Ranked by Distance + Availability + Urgency</p>
            </div>
          </div>

          <div className="space-y-3">
            {request.matches?.map((match, idx) => (
              <div
                key={idx}
                className={`p-5 rounded-2xl border transition-all ${
                  idx === 0
                    ? "bg-slate-900 border-rose-500/60 shadow-xl shadow-rose-950/30 ring-1 ring-rose-500/40"
                    : "bg-slate-900/80 border-slate-800 hover:border-slate-700"
                }`}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">
                        {match.resource_type === "blood_bank" ? "Blood Bank" : "Volunteer Donor"}
                      </span>
                      <span className="text-[10px] bg-emerald-500/20 text-emerald-300 font-bold px-1.5 py-0.5 rounded border border-emerald-500/30">
                        {match.availability_status}
                      </span>
                    </div>
                    <h4 className="font-bold text-sm text-white mt-1">{match.resource_name}</h4>
                    <p className="text-xs text-slate-400 mt-0.5">{match.address}</p>
                  </div>

                  {/* Match Score Badge */}
                  <div className="text-right">
                    <span className="text-lg font-black text-rose-400">{match.score}%</span>
                    <span className="block text-[10px] uppercase font-semibold text-slate-400">Match</span>
                  </div>
                </div>

                <div className="mt-3 flex items-center justify-between text-xs text-slate-300 pt-3 border-t border-slate-800/80">
                  <span>Proximity: <strong>{match.distance_km} km</strong> away</span>
                  {match.units_available !== undefined && (
                    <span className="text-slate-400">Stock: {match.units_available} Units</span>
                  )}
                </div>

                {/* Call and Directions Action Buttons */}
                <div className="mt-3 grid grid-cols-2 gap-2 pt-1">
                  <a
                    href={`tel:${match.contact_phone}`}
                    className="py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs flex items-center justify-center space-x-1 shadow-md shadow-rose-600/30 transition-colors"
                  >
                    <Phone className="w-3.5 h-3.5" />
                    <span>{match.contact_phone === "SECURE_MASKED_CONTACT" ? "Secure Call" : "Call Unit"}</span>
                  </a>
                  <a
                    href={`https://www.google.com/maps/dir/?api=1&destination=${match.latitude || 20.2961},${match.longitude || 85.8245}`}
                    target="_blank"
                    rel="noreferrer"
                    className="py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs flex items-center justify-center space-x-1 transition-colors"
                  >
                    <Navigation className="w-3.5 h-3.5" />
                    <span>Directions</span>
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: Embedded Map Radar */}
        <div className="lg:col-span-7">
          <div className="sticky top-24 space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-black text-white">Live Emergency Geo-Radar</h3>
              <span className="text-xs text-slate-400">Patient Hospital: {request.hospital_name}</span>
            </div>
            <EmergencyMap activeRequest={request} defaultCenter={[request.latitude, request.longitude]} />
          </div>
        </div>
      </div>
    </div>
  );
}
