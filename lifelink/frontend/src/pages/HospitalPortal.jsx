import React, { useEffect, useState } from "react";
import { 
  Building2, AlertTriangle, Activity, Truck, 
  CheckCircle2, Clock, Users, ArrowUpRight, RefreshCw 
} from "lucide-react";
import { api } from "../services/api";

export function HospitalPortal({ onSelectRequest }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchHospitalStats = async () => {
    try {
      setLoading(true);
      const res = await api.getHospitalDashboard();
      setData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHospitalStats();
  }, []);

  if (loading && !data) {
    return (
      <div className="py-24 text-center text-slate-400">
        <RefreshCw className="w-8 h-8 mx-auto animate-spin text-indigo-500 mb-2" />
        <p className="text-xs">Loading Hospital Triage Intelligence...</p>
      </div>
    );
  }

  const m = data?.metrics || { active_requests: 12, critical_cases: 3, blood_requests: 7, ambulances_available: 3 };
  const act = data?.todays_activity || { requests_received: 31, resolved: 26, pending: 5 };

  return (
    <div className="space-y-8 pb-16">
      {/* Top Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center space-x-2 bg-indigo-500/10 border border-indigo-500/30 px-3 py-1 rounded-full text-xs font-bold text-indigo-400 mb-2">
              <Building2 className="w-4 h-4 text-indigo-400" />
              <span>Apex Healthcare Portal & Triage Center</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-black text-white">Hospital Emergency Dashboard</h2>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              AIIMS Bhubaneswar &bull; Partner Network: Capital Hospital, Apollo, KIMS
            </p>
          </div>

          <button
            onClick={fetchHospitalStats}
            className="flex items-center space-x-2 bg-slate-800 hover:bg-slate-700 text-slate-300 px-4 py-2 rounded-xl text-xs font-bold transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Refresh Triage Data</span>
          </button>
        </div>
      </div>

      {/* METRICS CARDS (Exact Match to Specification Page 10) */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-3xl space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase tracking-wider">Active Requests</span>
            <Activity className="w-4 h-4 text-rose-500" />
          </div>
          <div className="text-3xl font-black text-white">{m.active_requests}</div>
          <p className="text-[11px] text-slate-400">Currently in triage queue</p>
        </div>

        <div className="bg-slate-900 border border-rose-500/40 p-6 rounded-3xl space-y-2 bg-gradient-to-b from-rose-950/20 to-slate-900">
          <div className="flex items-center justify-between text-rose-400">
            <span className="text-xs font-bold uppercase tracking-wider">Critical Cases</span>
            <AlertTriangle className="w-4 h-4 text-rose-400 animate-pulse" />
          </div>
          <div className="text-3xl font-black text-rose-400">{m.critical_cases}</div>
          <p className="text-[11px] text-rose-300/70">Requires sub-2hr fulfillment</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-6 rounded-3xl space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase tracking-wider">Blood Requests</span>
            <Activity className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-3xl font-black text-white">{m.blood_requests}</div>
          <p className="text-[11px] text-slate-400">RBC / Platelets / Plasma</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-6 rounded-3xl space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase tracking-wider">Ambulance Fleet</span>
            <Truck className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-3xl font-black text-amber-400">{m.ambulances_available} Available</div>
          <p className="text-[11px] text-slate-400">ALS & BLS units ready</p>
        </div>
      </div>

      {/* TODAY'S ACTIVITY (From Specification Page 10) */}
      <div className="grid md:grid-cols-12 gap-8">
        <div className="md:col-span-4 bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-6">
          <div className="border-b border-slate-800 pb-4">
            <h3 className="text-base font-black text-white">Today's Activity</h3>
            <p className="text-xs text-slate-400">Emergency fulfillment throughput</p>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between p-3.5 rounded-2xl bg-slate-800/40">
              <span className="text-xs text-slate-300 font-semibold">Requests Received</span>
              <span className="text-base font-black text-white">{act.requests_received}</span>
            </div>
            <div className="flex items-center justify-between p-3.5 rounded-2xl bg-emerald-950/30 border border-emerald-500/20">
              <span className="text-xs text-emerald-300 font-semibold">Resolved / Delivered</span>
              <span className="text-base font-black text-emerald-400">{act.resolved}</span>
            </div>
            <div className="flex items-center justify-between p-3.5 rounded-2xl bg-amber-950/30 border border-amber-500/20">
              <span className="text-xs text-amber-300 font-semibold">Pending Coordination</span>
              <span className="text-base font-black text-amber-400">{act.pending}</span>
            </div>
          </div>
        </div>

        {/* Recent Critical Requests Queue */}
        <div className="md:col-span-8 bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <h3 className="text-base font-black text-white">Live Hospital Triage Feed</h3>
              <p className="text-xs text-slate-400">Click any request to inspect matching resources</p>
            </div>
          </div>

          <div className="space-y-3">
            {data?.recent_requests?.map((req) => (
              <div
                key={req.request_code}
                onClick={() => onSelectRequest(req.request_code)}
                className="cursor-pointer bg-slate-800/50 hover:bg-slate-800 p-4 rounded-2xl border border-slate-700/60 flex items-center justify-between transition-colors"
              >
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-xs font-bold text-rose-400 bg-rose-500/10 px-2 py-0.5 rounded">
                      {req.request_code}
                    </span>
                    <span className="text-xs font-bold text-white">{req.patient}</span>
                    <span className="text-[10px] bg-red-500/20 text-red-400 px-2 py-0.5 rounded-full uppercase font-bold">
                      {req.urgency}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">
                    Needs: <strong>{req.units} Units</strong> of <strong>{req.blood_group}</strong> &bull; {req.hospital}
                  </p>
                </div>

                <div className="flex items-center space-x-3">
                  <span className="text-xs text-slate-400">{req.time}</span>
                  <div className="p-2 rounded-xl bg-slate-700 text-white">
                    <ArrowUpRight className="w-4 h-4" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
