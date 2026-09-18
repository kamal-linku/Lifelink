import React, { useEffect, useState } from "react";
import { 
  AlertOctagon, HeartHandshake, Droplet, Building2, 
  Truck, Pill, Users, ShieldAlert, PhoneCall, ArrowRight, Activity, MapPin 
} from "lucide-react";
import { api } from "../services/api";

export function Home({ onNavigate, onSelectRequest }) {
  const [stats, setStats] = useState({
    activeRequests: 1,
    bloodBanks: 4,
    ambulances: 3,
    volunteers: 6
  });
  const [recentRequests, setRecentRequests] = useState([]);

  useEffect(() => {
    async function loadData() {
      try {
        const reqs = await api.listRequests({ limit: 4 });
        setRecentRequests(reqs);
      } catch (err) {
        console.error("Failed loading home data", err);
      }
    }
    loadData();
  }, []);

  const resourceButtons = [
    { id: "blood-bank", label: "Blood Banks", icon: Droplet, count: "4 Verified", color: "from-rose-500/20 to-red-500/20 border-rose-500/30 text-rose-400" },
    { id: "hospital", label: "Hospitals", icon: Building2, count: "4 Apex Centers", color: "from-indigo-500/20 to-blue-500/20 border-indigo-500/30 text-indigo-400" },
    { id: "ambulances", label: "Ambulances", icon: Truck, count: "3 On-Duty", color: "from-amber-500/20 to-yellow-500/20 border-amber-500/30 text-amber-400" },
    { id: "pharmacies", label: "Pharmacies", icon: Pill, count: "3 24x7 Stocked", color: "from-emerald-500/20 to-teal-500/20 border-emerald-500/30 text-emerald-400" },
    { id: "volunteer", label: "Volunteers", icon: Users, count: "6 Active Donors", color: "from-purple-500/20 to-pink-500/20 border-purple-500/30 text-purple-400" },
    { id: "map", label: "Emergency Radar", icon: MapPin, count: "Live GPS Map", color: "from-cyan-500/20 to-sky-500/20 border-cyan-500/30 text-cyan-400" },
  ];

  return (
    <div className="space-y-12 pb-16">
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-b from-slate-900 via-slate-900 to-slate-950 border border-slate-800 p-8 sm:p-12 shadow-2xl">
        <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 bg-rose-600/10 rounded-full blur-3xl pointer-events-none" />
        <div className="max-w-3xl relative z-10">
          <div className="inline-flex items-center space-x-2 bg-rose-500/10 border border-rose-500/30 px-3 py-1 rounded-full text-xs font-bold text-rose-400 mb-6">
            <Activity className="w-4 h-4 animate-pulse" />
            <span>AIIMS & Central Red Cross Coordinated Network</span>
          </div>

          <h1 className="text-4xl sm:text-5xl font-black text-white tracking-tight leading-tight">
            Our problem is not simply finding a donor. <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-rose-400 via-red-300 to-amber-300">
              It is coordinating the entire emergency response quickly.
            </span>
          </h1>

          <p className="mt-4 text-base sm:text-lg text-slate-300 leading-relaxed">
            LifeLink instantly unites patient blood requirements, verified blood bank inventories, hospital ICUs, ambulances, and voluntary donors within minutes using geo-ranking.
          </p>

          {/* TWO PRIMARY ACTIONS (From Specification) */}
          <div className="mt-8 grid sm:grid-cols-2 gap-4">
            <button
              onClick={() => onNavigate("create-request")}
              className="flex items-center justify-between p-5 rounded-2xl bg-gradient-to-r from-rose-600 to-red-600 hover:from-rose-500 hover:to-red-500 text-white shadow-xl shadow-rose-600/30 border border-rose-400/30 group transition-all transform hover:-translate-y-0.5"
            >
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center">
                  <AlertOctagon className="w-7 h-7 text-white animate-bounce" />
                </div>
                <div className="text-left">
                  <span className="text-xs uppercase font-black tracking-widest text-rose-200">Critical Dispatch</span>
                  <h3 className="text-lg font-black text-white">I NEED HELP</h3>
                  <p className="text-xs text-rose-100">Create Emergency Blood / Resource Request</p>
                </div>
              </div>
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </button>

            <button
              onClick={() => onNavigate("volunteer")}
              className="flex items-center justify-between p-5 rounded-2xl bg-gradient-to-r from-emerald-700 to-teal-700 hover:from-emerald-600 hover:to-teal-600 text-white shadow-xl shadow-emerald-700/30 border border-emerald-400/30 group transition-all transform hover:-translate-y-0.5"
            >
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center">
                  <HeartHandshake className="w-7 h-7 text-white" />
                </div>
                <div className="text-left">
                  <span className="text-xs uppercase font-black tracking-widest text-emerald-200">Save a Life</span>
                  <h3 className="text-lg font-black text-white">I CAN HELP</h3>
                  <p className="text-xs text-emerald-100">Register as Verified Volunteer Donor</p>
                </div>
              </div>
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </button>
          </div>
        </div>
      </section>

      {/* Resource Quick Directory */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-black text-white tracking-tight">Emergency Resource Directory</h2>
            <p className="text-xs text-slate-400">Verified medical institutions and assets across Bhubaneswar</p>
          </div>
          <button
            onClick={() => onNavigate("map")}
            className="text-xs font-bold text-rose-400 hover:text-rose-300 flex items-center space-x-1"
          >
            <span>View All on Radar Map</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {resourceButtons.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={`p-4 rounded-2xl bg-gradient-to-b ${item.color} border text-left hover:scale-[1.02] transition-all flex flex-col justify-between h-32`}
              >
                <div className="w-9 h-9 rounded-xl bg-slate-900/60 flex items-center justify-center">
                  <Icon className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="font-bold text-sm text-white">{item.label}</h4>
                  <p className="text-[11px] text-slate-400 mt-0.5">{item.count}</p>
                </div>
              </button>
            );
          })}
        </div>
      </section>

      {/* Active Requests Feed */}
      <section className="bg-slate-900/70 border border-slate-800 rounded-3xl p-6 sm:p-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="w-3 h-3 rounded-full bg-rose-500 animate-ping" />
            <h3 className="text-lg font-black text-white">Live Emergency Feed</h3>
          </div>
          <span className="text-xs bg-slate-800 text-slate-300 px-3 py-1 rounded-full border border-slate-700">
            Real-Time Coordination
          </span>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          {recentRequests.map((req) => (
            <div
              key={req.request_code}
              onClick={() => onSelectRequest(req.request_code)}
              className="cursor-pointer bg-slate-850 hover:bg-slate-800/80 p-5 rounded-2xl border border-slate-800 transition-all hover:border-slate-700 space-y-3"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold text-rose-400 bg-rose-500/10 px-2.5 py-1 rounded-md border border-rose-500/20">
                  {req.request_code}
                </span>
                <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full uppercase ${
                  req.urgency.toLowerCase() === "critical"
                    ? "bg-red-500/20 text-red-400 border border-red-500/30"
                    : "bg-amber-500/20 text-amber-400"
                }`}>
                  {req.urgency}
                </span>
              </div>

              <div>
                <h4 className="text-base font-bold text-white">{req.patient_name}</h4>
                <p className="text-xs text-slate-400">{req.hospital_name}, {req.city}</p>
              </div>

              <div className="flex items-center justify-between pt-2 border-t border-slate-800 text-xs text-slate-300">
                <span className="font-semibold text-rose-300">
                  Required: {req.units_needed} Units ({req.blood_group} {req.component})
                </span>
                <span className="text-[11px] text-slate-400">
                  Status: <strong className="text-white">{req.status}</strong> &rarr;
                </span>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
