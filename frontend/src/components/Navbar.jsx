import React from "react";
import { Activity, Heart, ShieldAlert, PhoneCall, MapPin, Building2, Droplet, Truck, Pill } from "lucide-react";

export function Navbar({ currentTab, setCurrentTab }) {
  const navItems = [
    { id: "home", label: "Overview", icon: Activity },
    { id: "create-request", label: "Request Emergency", icon: ShieldAlert, highlight: true },
    { id: "map", label: "Emergency Radar", icon: MapPin },
    { id: "volunteer", label: "Volunteer Portal", icon: Heart },
    { id: "hospital", label: "Hospital Portal", icon: Building2 },
    { id: "blood-bank", label: "Blood Inventory", icon: Droplet },
    { id: "ambulances", label: "Ambulances", icon: Truck },
    { id: "pharmacies", label: "Pharmacies", icon: Pill },
  ];

  return (
    <header className="sticky top-0 z-50 bg-slate-900/95 backdrop-blur border-b border-slate-800 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <div 
            onClick={() => setCurrentTab("home")} 
            className="flex items-center space-x-3 cursor-pointer group"
          >
            <div className="relative w-10 h-10 rounded-xl bg-gradient-to-tr from-rose-600 to-red-500 flex items-center justify-center shadow-lg shadow-rose-900/30 group-hover:scale-105 transition-transform">
              <Activity className="w-6 h-6 text-white" />
              <span className="absolute -top-1 -right-1 flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-rose-500"></span>
              </span>
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xl font-black tracking-tight text-white">LIFELINK</span>
                <span className="bg-rose-500/20 text-rose-400 border border-rose-500/30 text-[10px] font-semibold px-2 py-0.5 rounded-full">
                  LIVE DISPATCH
                </span>
              </div>
              <p className="text-[11px] text-slate-400">Emergency Resource Coordination Network</p>
            </div>
          </div>

          {/* Nav Items */}
          <nav className="hidden lg:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentTab === item.id;
              if (item.highlight) {
                return (
                  <button
                    key={item.id}
                    onClick={() => setCurrentTab(item.id)}
                    className={`ml-2 px-3 py-2 rounded-lg text-sm font-bold flex items-center space-x-1.5 transition-all ${
                      isActive
                        ? "bg-rose-600 text-white shadow-md shadow-rose-600/40"
                        : "bg-rose-500 hover:bg-rose-600 text-white animate-pulse"
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{item.label}</span>
                  </button>
                );
              }
              return (
                <button
                  key={item.id}
                  onClick={() => setCurrentTab(item.id)}
                  className={`px-3 py-2 rounded-lg text-xs font-medium flex items-center space-x-1.5 transition-colors ${
                    isActive
                      ? "bg-slate-800 text-white border border-slate-700"
                      : "text-slate-300 hover:bg-slate-800/60 hover:text-white"
                  }`}
                >
                  <Icon className="w-3.5 h-3.5 opacity-80" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Quick Emergency Hotline */}
          <div className="flex items-center space-x-3">
            <a
              href="tel:108"
              className="flex items-center space-x-1.5 bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 px-3 py-1.5 rounded-lg text-xs font-bold transition-all"
            >
              <PhoneCall className="w-3.5 h-3.5 animate-bounce" />
              <span>SOS 108</span>
            </a>
          </div>
        </div>

        {/* Mobile scroll nav */}
        <div className="lg:hidden flex items-center space-x-2 py-2 overflow-x-auto no-scrollbar border-t border-slate-800/50">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setCurrentTab(item.id)}
              className={`px-2.5 py-1.5 rounded-md text-xs font-medium whitespace-nowrap ${
                currentTab === item.id
                  ? "bg-rose-600 text-white"
                  : "bg-slate-800 text-slate-300"
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>
      </div>
    </header>
  );
}
