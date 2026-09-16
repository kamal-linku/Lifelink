import React, { useEffect, useState } from "react";
import { Truck, Phone, Navigation, ShieldCheck, CheckCircle2, Clock } from "lucide-react";
import { api } from "../services/api";

export function AmbulanceDirectory() {
  const [ambulances, setAmbulances] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dispatchedId, setDispatchedId] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await api.getAmbulances();
        setAmbulances(data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const handleDispatch = (id) => {
    setDispatchedId(id);
    setTimeout(() => setDispatchedId(null), 6000);
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8 pb-16">
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl">
        <div className="inline-flex items-center space-x-2 bg-amber-500/10 border border-amber-500/30 px-3 py-1 rounded-full text-xs font-bold text-amber-400 mb-2">
          <Truck className="w-4 h-4 text-amber-400" />
          <span>Rapid Response Fleet</span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-black text-white">Ambulance Dispatch Module</h2>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Instant connection to Advanced Life Support (ALS) and Basic Life Support (BLS) emergency vehicles.
        </p>
      </div>

      {dispatchedId && (
        <div className="p-4 bg-emerald-950/60 border border-emerald-500/60 rounded-2xl text-emerald-300 text-xs font-bold flex items-center space-x-2">
          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          <span>Ambulance dispatch signal broadcasted to driver. GPS tracking active!</span>
        </div>
      )}

      <div className="grid md:grid-cols-3 gap-6">
        {ambulances.map((amb) => (
          <div
            key={amb.id}
            className="bg-slate-900 border border-slate-800 p-6 rounded-3xl shadow-xl space-y-4 hover:border-slate-700 transition-all flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-amber-400 bg-amber-500/10 px-2.5 py-1 rounded-lg border border-amber-500/20">
                  {amb.vehicle_number}
                </span>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase ${
                  amb.is_available ? "bg-emerald-500/20 text-emerald-400" : "bg-red-500/20 text-red-400"
                }`}>
                  {amb.is_available ? "Available" : "On Trip"}
                </span>
              </div>

              <div>
                <h4 className="font-bold text-base text-white">{amb.provider_name}</h4>
                <p className="text-xs text-slate-400 mt-0.5">{amb.ambulance_type}</p>
              </div>

              <div className="bg-slate-800/60 p-3 rounded-xl text-xs space-y-1 text-slate-300">
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Driver:</span>
                  <span className="font-semibold text-white flex items-center">
                    <ShieldCheck className="w-3.5 h-3.5 text-emerald-400 mr-1" />
                    {amb.driver_name}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Hub:</span>
                  <span>{amb.city}</span>
                </div>
              </div>
            </div>

            <div className="space-y-2 pt-2 border-t border-slate-800">
              <button
                onClick={() => handleDispatch(amb.id)}
                disabled={!amb.is_available}
                className="w-full py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 disabled:opacity-40 text-slate-950 font-black text-xs flex items-center justify-center space-x-1 shadow-lg shadow-amber-500/20 transition-all"
              >
                <Truck className="w-4 h-4" />
                <span>REQUEST DISPATCH</span>
              </button>
              <a
                href={`tel:${amb.contact_phone}`}
                className="w-full py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs flex items-center justify-center space-x-1 transition-colors"
              >
                <Phone className="w-3.5 h-3.5" />
                <span>Secure Driver Call</span>
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
