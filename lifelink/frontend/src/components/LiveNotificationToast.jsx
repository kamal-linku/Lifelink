import React, { useEffect } from "react";
import { Bell, X, AlertTriangle, CheckCircle, ShieldAlert } from "lucide-react";

export function LiveNotificationToast({ notification, onClose, onAction }) {
  if (!notification) return null;

  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, 8000);
    return () => clearTimeout(timer);
  }, [notification, onClose]);

  const isEmergency = notification.event === "EMERGENCY_CREATED";
  const isAccept = notification.event === "VOLUNTEER_ACCEPTED";

  return (
    <div className="fixed bottom-6 right-6 z-[9999] max-w-md w-full animate-bounce-once">
      <div className={`rounded-2xl p-4 shadow-2xl border backdrop-blur-lg text-white ${
        isEmergency
          ? "bg-rose-950/90 border-rose-500 shadow-rose-900/40"
          : isAccept
          ? "bg-emerald-950/90 border-emerald-500 shadow-emerald-900/40"
          : "bg-slate-900/90 border-slate-700 shadow-black/40"
      }`}>
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-3">
            <div className={`w-9 h-9 rounded-xl flex items-center justify-center ${
              isEmergency ? "bg-rose-600 text-white" : isAccept ? "bg-emerald-600 text-white" : "bg-slate-800 text-slate-300"
            }`}>
              {isEmergency ? <ShieldAlert className="w-5 h-5 animate-pulse" /> : <CheckCircle className="w-5 h-5" />}
            </div>
            <div>
              <span className={`text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full ${
                isEmergency ? "bg-rose-500/20 text-rose-300" : "bg-emerald-500/20 text-emerald-300"
              }`}>
                {notification.event ? notification.event.replace("_", " ") : "SYSTEM ALERT"}
              </span>
              <h5 className="font-bold text-sm text-white mt-0.5">
                {isEmergency ? `Emergency Dispatch: ${notification.request_code}` : "Volunteer Response"}
              </h5>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="mt-2 text-xs text-slate-200">
          {isEmergency && (
            <p>
              Urgent request for <strong>{notification.units} units of {notification.blood_group} ({notification.component})</strong> at {notification.hospital}.
            </p>
          )}
          {isAccept && (
            <p>
              Volunteer <strong>{notification.donor_display_name}</strong> ({notification.blood_group}) has accepted request <strong>{notification.request_code}</strong>.
            </p>
          )}
        </div>

        {onAction && (
          <div className="mt-3 flex justify-end">
            <button
              onClick={onAction}
              className="bg-white text-slate-900 hover:bg-slate-200 font-bold text-xs px-3 py-1.5 rounded-lg shadow transition-colors"
            >
              View Details &rarr;
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
