import React from "react";
import { CheckCircle2, Clock, Search, PhoneForwarded, Users, ShieldCheck, Award } from "lucide-react";

export function WorkflowTracker({ currentStatus = "MATCHING", assignedResource = "", onRequestStatusUpdate }) {
  const steps = [
    { key: "MATCHING", label: "Matching", desc: "Engine scanning resources", icon: Search },
    { key: "CONTACTED", label: "Blood Bank Contacted", desc: "Inventory alert dispatched", icon: PhoneForwarded },
    { key: "RESPONDED", label: "Volunteer Response", desc: "Donor accepted dispatch", icon: Users },
    { key: "CONFIRMED", label: "Resource Confirmed", desc: "Unit reserved & in-transit", icon: ShieldCheck },
    { key: "COMPLETED", label: "Completed", desc: "Transfusion delivered", icon: Award },
  ];

  const getStepIndex = (status) => {
    const idx = steps.findIndex((s) => s.key === status);
    return idx === -1 ? 0 : idx;
  };

  const currentIdx = getStepIndex(currentStatus);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl text-white">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
        <div>
          <span className="text-xs font-bold text-rose-500 uppercase tracking-wider">Workflow Engine</span>
          <h3 className="text-lg font-black text-white">Emergency Response Pipeline</h3>
        </div>
        <div className="flex items-center space-x-2 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
          <Clock className="w-4 h-4 text-amber-400 animate-spin" />
          <span className="text-xs font-semibold text-slate-300">Live Coordination</span>
        </div>
      </div>

      {/* Stepper Bar */}
      <div className="relative">
        {/* Track Line */}
        <div className="absolute top-5 left-6 right-6 h-1 bg-slate-800 -z-0">
          <div
            className="h-full bg-gradient-to-r from-rose-500 to-emerald-500 transition-all duration-500"
            style={{ width: `${(currentIdx / (steps.length - 1)) * 100}%` }}
          />
        </div>

        {/* Step Nodes */}
        <div className="relative z-10 grid grid-cols-5 gap-2">
          {steps.map((step, index) => {
            const Icon = step.icon;
            const isCompleted = index < currentIdx;
            const isCurrent = index === currentIdx;

            return (
              <div key={step.key} className="flex flex-col items-center text-center">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center transition-all duration-300 ${
                    isCompleted
                      ? "bg-emerald-500 text-white shadow-lg shadow-emerald-500/30 ring-2 ring-emerald-400"
                      : isCurrent
                      ? "bg-rose-600 text-white shadow-lg shadow-rose-600/40 ring-4 ring-rose-500/30 animate-pulse"
                      : "bg-slate-800 text-slate-500 border border-slate-700"
                  }`}
                >
                  {isCompleted ? <CheckCircle2 className="w-5 h-5" /> : <Icon className="w-5 h-5" />}
                </div>
                <h5 className={`text-xs font-bold mt-2.5 ${isCurrent ? "text-rose-400" : isCompleted ? "text-emerald-400" : "text-slate-400"}`}>
                  {step.label}
                </h5>
                <p className="text-[10px] text-slate-500 hidden sm:block mt-0.5 max-w-[100px] leading-tight">
                  {step.desc}
                </p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Assigned Resource Callout */}
      {assignedResource && (
        <div className="mt-6 bg-emerald-950/40 border border-emerald-500/40 rounded-xl p-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs text-emerald-400 font-bold uppercase tracking-wider">Assigned Coordinator</p>
              <p className="text-sm font-semibold text-white">{assignedResource}</p>
            </div>
          </div>
          <span className="text-xs bg-emerald-500/20 text-emerald-300 px-2.5 py-1 rounded-full border border-emerald-500/30 font-semibold">
            In Transit / Reserved
          </span>
        </div>
      )}

      {/* Manual Step Advancement (for Live Viva Demonstration) */}
      {onRequestStatusUpdate && (
        <div className="mt-6 pt-4 border-t border-slate-800 flex flex-wrap items-center justify-between gap-2">
          <span className="text-xs text-slate-400">Simulation Control:</span>
          <div className="flex flex-wrap items-center gap-2">
            {steps.map((s) => (
              <button
                key={s.key}
                onClick={() => onRequestStatusUpdate(s.key)}
                className={`text-[11px] px-2.5 py-1 rounded-md font-medium border transition-colors ${
                  s.key === currentStatus
                    ? "bg-rose-600 text-white border-rose-500"
                    : "bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700"
                }`}
              >
                Mark {s.label}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
