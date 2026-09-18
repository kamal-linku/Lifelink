import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, Circle } from "react-leaflet";
import L from "leaflet";
import { Filter, Layers, Navigation, Phone, CheckCircle2, AlertCircle } from "lucide-react";
import { api } from "../services/api";

// Helper to create beautiful custom HTML markers without relying on external image asset paths
const createCustomIcon = (type, label = "") => {
  let bgClass = "bg-rose-600";
  let symbol = "🩸";

  if (type === "hospital") {
    bgClass = "bg-indigo-600";
    symbol = "🏥";
  } else if (type === "blood_bank") {
    bgClass = "bg-rose-600";
    symbol = "🩸";
  } else if (type === "ambulance") {
    bgClass = "bg-amber-500";
    symbol = "🚑";
  } else if (type === "volunteer") {
    bgClass = "bg-emerald-600";
    symbol = "❤️";
  } else if (type === "patient") {
    bgClass = "bg-red-700 animate-pulse";
    symbol = "🆘";
  }

  const html = `
    <div class="relative flex items-center justify-center">
      <div class="w-8 h-8 rounded-full ${bgClass} text-white flex items-center justify-center text-sm shadow-lg border-2 border-white ring-2 ring-black/20 transform hover:scale-110 transition-transform">
        <span>${symbol}</span>
      </div>
      ${label ? `<span class="absolute -bottom-4 bg-slate-900 text-white text-[10px] font-bold px-1.5 py-0.5 rounded shadow whitespace-nowrap">${label}</span>` : ""}
    </div>
  `;

  return L.divIcon({
    html: html,
    className: "custom-leaflet-marker",
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -18],
  });
};

export function EmergencyMap({ activeRequest = null, defaultCenter = [20.2961, 85.8245] }) {
  const [markers, setMarkers] = useState([]);
  const [filterType, setFilterType] = useState("all");
  const [selectedBloodGroup, setSelectedBloodGroup] = useState("");
  const [loading, setLoading] = useState(true);

  const fetchMarkers = async () => {
    try {
      setLoading(true);
      const params = {};
      if (filterType !== "all") params.resource_type = filterType;
      if (selectedBloodGroup) params.blood_group = selectedBloodGroup;
      const data = await api.getMapResources(params);
      setMarkers(data);
    } catch (err) {
      console.error("Failed to load map markers", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMarkers();
  }, [filterType, selectedBloodGroup]);

  const centerCoords = activeRequest?.latitude && activeRequest?.longitude
    ? [activeRequest.latitude, activeRequest.longitude]
    : defaultCenter;

  return (
    <div className="relative w-full h-[650px] rounded-2xl overflow-hidden border border-slate-700/60 shadow-2xl bg-slate-900">
      {/* Top Filter Overlay */}
      <div className="absolute top-4 left-4 right-4 z-[1000] flex flex-wrap items-center justify-between gap-2 bg-slate-900/90 backdrop-blur-md p-3 rounded-xl border border-slate-800 shadow-xl">
        <div className="flex items-center space-x-2">
          <div className="bg-rose-500/20 p-1.5 rounded-lg border border-rose-500/30">
            <Layers className="w-4 h-4 text-rose-400" />
          </div>
          <div>
            <h4 className="text-xs font-bold text-white uppercase tracking-wider">Emergency Radar</h4>
            <p className="text-[10px] text-slate-400">Live Resource Geo-Coordination (Bhubaneswar Hub)</p>
          </div>
        </div>

        {/* Filter Buttons */}
        <div className="flex flex-wrap items-center gap-1.5 text-xs">
          {[
            { id: "all", label: "All Units", icon: "🌐" },
            { id: "blood_bank", label: "Blood Banks", icon: "🩸" },
            { id: "hospital", label: "Hospitals", icon: "🏥" },
            { id: "ambulance", label: "Ambulances", icon: "🚑" },
            { id: "volunteer", label: "Volunteers", icon: "❤️" },
          ].map((btn) => (
            <button
              key={btn.id}
              onClick={() => setFilterType(btn.id)}
              className={`px-2.5 py-1 rounded-lg font-medium transition-colors flex items-center space-x-1 ${
                filterType === btn.id
                  ? "bg-rose-600 text-white shadow-sm"
                  : "bg-slate-800 text-slate-300 hover:bg-slate-700"
              }`}
            >
              <span>{btn.icon}</span>
              <span>{btn.label}</span>
            </button>
          ))}

          {/* Blood group filter selector */}
          <select
            value={selectedBloodGroup}
            onChange={(e) => setSelectedBloodGroup(e.target.value)}
            className="bg-slate-800 text-white text-xs border border-slate-700 rounded-lg px-2 py-1 focus:outline-none focus:ring-1 focus:ring-rose-500 ml-1"
          >
            <option value="">Blood: All</option>
            {["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"].map((bg) => (
              <option key={bg} value={bg}>{bg}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Map Container */}
      <MapContainer
        center={centerCoords}
        zoom={12}
        scrollWheelZoom={true}
        className="w-full h-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Active Patient Marker if in Request View */}
        {activeRequest && (
          <>
            <Circle
              center={[activeRequest.latitude, activeRequest.longitude]}
              radius={3000}
              pathOptions={{ color: "red", fillColor: "red", fillOpacity: 0.15 }}
            />
            <Marker
              position={[activeRequest.latitude, activeRequest.longitude]}
              icon={createCustomIcon("patient", "URGENT PATIENT")}
            >
              <Popup>
                <div className="p-1 max-w-[200px]">
                  <span className="bg-red-600 text-white text-[10px] font-bold px-1.5 py-0.5 rounded uppercase">
                    Critical Emergency
                  </span>
                  <h5 className="font-bold text-sm text-slate-900 mt-1">{activeRequest.patient_name}</h5>
                  <p className="text-xs text-slate-600">Hospital: {activeRequest.hospital_name}</p>
                  <p className="text-xs font-bold text-red-600 mt-1">
                    Need: {activeRequest.units_needed} Units ({activeRequest.blood_group} {activeRequest.component})
                  </p>
                </div>
              </Popup>
            </Marker>
          </>
        )}

        {/* Resource Markers */}
        {markers.map((m) => (
          <Marker
            key={m.id}
            position={[m.latitude, m.longitude]}
            icon={createCustomIcon(m.type)}
          >
            <Popup>
              <div className="p-2 min-w-[220px]">
                <div className="flex items-center justify-between border-b pb-1 mb-2">
                  <span className="text-[10px] uppercase font-bold text-slate-500 tracking-wider">
                    {m.type.replace("_", " ")}
                  </span>
                  {m.is_verified && (
                    <span className="flex items-center text-[10px] text-emerald-600 font-semibold">
                      <CheckCircle2 className="w-3 h-3 mr-0.5" /> Verified
                    </span>
                  )}
                </div>

                <h4 className="font-bold text-sm text-slate-900 leading-snug">{m.name}</h4>
                {m.address && <p className="text-xs text-slate-500 mt-0.5">{m.address}</p>}

                <div className="mt-2 bg-slate-100 p-1.5 rounded text-xs text-slate-700">
                  <p className="font-semibold text-rose-700">Status: {m.status}</p>
                  {m.details?.ambulance_type && <p>Type: {m.details.ambulance_type}</p>}
                  {m.details?.icu_available !== undefined && (
                    <p>ICU Beds: {m.details.icu_available} / {m.details.total_beds}</p>
                  )}
                </div>

                <div className="mt-3 flex items-center justify-between gap-1 pt-1 border-t">
                  <a
                    href={`tel:${m.contact}`}
                    className="flex-1 text-center bg-rose-600 hover:bg-rose-700 text-white text-xs font-semibold py-1 px-2 rounded flex items-center justify-center space-x-1"
                  >
                    <Phone className="w-3 h-3" />
                    <span>{m.contact === "Secure Masked Call" ? "Secure Call" : "Call"}</span>
                  </a>
                  <a
                    href={`https://www.google.com/maps/dir/?api=1&destination=${m.latitude},${m.longitude}`}
                    target="_blank"
                    rel="noreferrer"
                    className="flex-1 text-center bg-slate-800 hover:bg-slate-900 text-white text-xs font-semibold py-1 px-2 rounded flex items-center justify-center space-x-1"
                  >
                    <Navigation className="w-3 h-3" />
                    <span>Directions</span>
                  </a>
                </div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>

      {/* Bottom Status Legend */}
      <div className="absolute bottom-4 left-4 z-[1000] bg-slate-900/90 backdrop-blur-md px-3 py-2 rounded-xl border border-slate-800 text-[11px] text-slate-300 flex items-center space-x-4 shadow-lg">
        <span className="flex items-center space-x-1"><span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span> <span>Blood Bank</span></span>
        <span className="flex items-center space-x-1"><span className="w-2.5 h-2.5 rounded-full bg-indigo-500"></span> <span>Hospital</span></span>
        <span className="flex items-center space-x-1"><span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span> <span>Ambulance</span></span>
        <span className="flex items-center space-x-1"><span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> <span>Volunteer</span></span>
      </div>
    </div>
  );
}
