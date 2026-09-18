import React, { useEffect, useState } from "react";
import { Pill, Search, Clock, Phone, MapPin, AlertCircle, ShieldCheck } from "lucide-react";
import { api } from "../services/api";

export function PharmacyDirectory() {
  const [pharmacies, setPharmacies] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await api.getPharmacies();
        setPharmacies(data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const filtered = pharmacies.filter((p) =>
    searchTerm === "" ||
    p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.inventory_notes.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="max-w-5xl mx-auto space-y-8 pb-16">
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl">
        <div className="inline-flex items-center space-x-2 bg-emerald-500/10 border border-emerald-500/30 px-3 py-1 rounded-full text-xs font-bold text-emerald-400 mb-2">
          <Pill className="w-4 h-4 text-emerald-400" />
          <span>Critical Medicine & Coagulant Availability</span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-black text-white">Emergency Pharmacy Network</h2>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Locate critical coagulants, IV solutions, and life-saving medications in Bhubaneswar.
        </p>

        {/* Search Bar */}
        <div className="mt-6 relative">
          <Search className="w-5 h-5 text-slate-400 absolute left-4 top-3.5" />
          <input
            type="text"
            placeholder="Search critical drug (e.g. Tranexamic Acid, Albumin, Heparin, Saline)..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-12 pr-4 py-3 bg-slate-800 border border-slate-700 rounded-2xl text-white text-sm focus:outline-none focus:border-rose-500"
          />
        </div>
      </div>

      {/* Mandatory Stock Disclaimer (Specification Page 12) */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 flex items-start space-x-3 text-slate-400 text-xs">
        <AlertCircle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
        <p>
          <strong className="text-amber-400">Stock Freshness Notice:</strong> Emergency pharmacies continuously update availability. Medicine availability is reported as recent telemetry and does not constitute guaranteed warehouse reservation until confirmed over direct telephone.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {filtered.map((ph) => (
          <div
            key={ph.id}
            className="bg-slate-900 border border-slate-800 p-6 rounded-3xl shadow-xl space-y-4 hover:border-slate-700 transition-all flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">
                  {ph.is_24x7 ? "24x7 Open" : "Day Shift"}
                </span>
                <span className="text-[11px] font-semibold text-slate-400 flex items-center">
                  <Clock className="w-3.5 h-3.5 mr-1 text-slate-500" />
                  Reported {ph.last_verified_minutes_ago}m ago
                </span>
              </div>

              <div>
                <h4 className="font-bold text-base text-white">{ph.name}</h4>
                <p className="text-xs text-slate-400 mt-1 flex items-start">
                  <MapPin className="w-3.5 h-3.5 mr-1 text-slate-500 flex-shrink-0 mt-0.5" />
                  {ph.address}
                </p>
              </div>

              <div className="bg-slate-800/60 p-3 rounded-xl text-xs space-y-1 text-slate-300">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Reported Stock:</span>
                <p className="text-emerald-300 font-semibold">{ph.inventory_notes}</p>
              </div>
            </div>

            <div className="pt-2 border-t border-slate-800">
              <a
                href={`tel:${ph.contact_phone}`}
                className="w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-black text-xs flex items-center justify-center space-x-1 shadow-lg shadow-emerald-600/20 transition-all"
              >
                <Phone className="w-3.5 h-3.5" />
                <span>Call Pharmacy ({ph.contact_phone})</span>
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
