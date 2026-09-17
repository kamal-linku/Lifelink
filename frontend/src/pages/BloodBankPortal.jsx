import React, { useEffect, useState } from "react";
import { Droplet, Plus, Minus, CheckCircle2, RefreshCw, Layers, ShieldCheck } from "lucide-react";
import { api } from "../services/api";

export function BloodBankPortal() {
  const [bloodBanks, setBloodBanks] = useState([]);
  const [selectedBankId, setSelectedBankId] = useState(1);
  const [inventory, setInventory] = useState([]);
  const [selectedComponent, setSelectedComponent] = useState("Packed RBC");
  const [loading, setLoading] = useState(true);
  const [updateMessage, setUpdateMessage] = useState("");

  const bloodGroups = ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"];
  const components = ["Packed RBC", "Platelets", "Plasma", "Whole Blood"];

  const loadData = async () => {
    try {
      setLoading(true);
      const banks = await api.getBloodBanks();
      setBloodBanks(banks);
      if (banks.length > 0) {
        const current = banks.find((b) => b.id === selectedBankId) || banks[0];
        setInventory(current.inventory || []);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [selectedBankId]);

  const handleStockDelta = async (group, delta) => {
    try {
      await api.updateInventory(selectedBankId, group, selectedComponent, delta);
      setUpdateMessage(`Updated ${group} (${selectedComponent}) stock by ${delta > 0 ? "+" + delta : delta}`);
      setTimeout(() => setUpdateMessage(""), 4000);
      await loadData();
    } catch (err) {
      alert("Inventory update error: " + err.message);
    }
  };

  const getUnitsFor = (grp) => {
    const item = inventory.find(
      (i) => i.blood_group === grp && i.component === selectedComponent
    );
    return item ? item.units_available : 0;
  };

  const currentBank = bloodBanks.find((b) => b.id === selectedBankId) || bloodBanks[0];

  return (
    <div className="max-w-5xl mx-auto space-y-8 pb-16">
      {/* Top Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center space-x-2 bg-rose-500/10 border border-rose-500/30 px-3 py-1 rounded-full text-xs font-bold text-rose-400 mb-2">
              <Droplet className="w-4 h-4 text-rose-500" />
              <span>e-RaktKosh Aligned Blood Inventory Engine</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-black text-white">Blood Bank Inventory Hub</h2>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Synchronized multi-component tracking: Packed RBC, Platelets, Plasma, Whole Blood.
            </p>
          </div>

          {/* Select Blood Bank Institution */}
          <div className="bg-slate-800/80 p-2 rounded-2xl border border-slate-700 flex items-center space-x-2">
            <span className="text-xs text-slate-400 pl-2">Select Center:</span>
            <select
              value={selectedBankId}
              onChange={(e) => setSelectedBankId(parseInt(e.target.value))}
              className="bg-slate-900 text-white text-xs font-bold rounded-xl px-3 py-2 border border-slate-600 focus:outline-none focus:border-rose-500"
            >
              {bloodBanks.map((b) => (
                <option key={b.id} value={b.id}>
                  {b.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Institution Verification Badge */}
        {currentBank && (
          <div className="mt-6 pt-4 border-t border-slate-800 flex flex-wrap items-center justify-between gap-2 text-xs text-slate-400">
            <div className="flex items-center space-x-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span className="font-bold text-white">{currentBank.name}</span>
              <span className="bg-emerald-500/20 text-emerald-300 font-bold px-2 py-0.5 rounded-full border border-emerald-500/30">
                VERIFIED ORGANIZATION
              </span>
            </div>
            <span>License: {currentBank.license_no || "BB-OD-GOVT"} &bull; {currentBank.operating_hours}</span>
          </div>
        )}
      </div>

      {updateMessage && (
        <div className="p-3 bg-emerald-950/60 border border-emerald-500/50 rounded-2xl text-xs font-bold text-emerald-300 flex items-center space-x-2">
          <CheckCircle2 className="w-4 h-4" />
          <span>{updateMessage}</span>
        </div>
      )}

      {/* Component Tabs (Packed RBC, Platelets, Plasma, Whole Blood) */}
      <div className="flex flex-wrap items-center gap-2">
        {components.map((c) => (
          <button
            key={c}
            onClick={() => setSelectedComponent(c)}
            className={`px-4 py-2.5 rounded-2xl font-bold text-xs transition-all flex items-center space-x-2 ${
              selectedComponent === c
                ? "bg-rose-600 text-white shadow-lg shadow-rose-600/30 ring-2 ring-rose-400/40"
                : "bg-slate-900 text-slate-400 border border-slate-800 hover:bg-slate-800 hover:text-white"
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>{c}</span>
          </button>
        ))}
      </div>

      {/* BLOOD INVENTORY GRID (Exact Match to Specification Page 10) */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {bloodGroups.map((grp) => {
          const units = getUnitsFor(grp);
          const isLow = units < 3;
          return (
            <div
              key={grp}
              className={`p-6 rounded-3xl border shadow-xl transition-all space-y-4 ${
                isLow
                  ? "bg-gradient-to-b from-rose-950/40 to-slate-900 border-rose-500/50"
                  : "bg-slate-900 border-slate-800"
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-2xl font-black text-white">{grp}</span>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase ${
                  isLow ? "bg-rose-500/20 text-rose-400 border border-rose-500/30" : "bg-emerald-500/20 text-emerald-400"
                }`}>
                  {isLow ? "Low Stock" : "Available"}
                </span>
              </div>

              <div>
                <span className="text-4xl font-black text-white">{units}</span>
                <span className="text-xs text-slate-400 ml-1.5 font-semibold">Units</span>
              </div>

              {/* Staff Stock Delta Buttons */}
              <div className="flex items-center space-x-2 pt-2 border-t border-slate-800">
                <button
                  onClick={() => handleStockDelta(grp, -1)}
                  disabled={units <= 0}
                  className="flex-1 py-1.5 bg-slate-800 hover:bg-slate-700 disabled:opacity-30 text-white rounded-xl flex items-center justify-center transition-colors"
                  title="Release 1 unit"
                >
                  <Minus className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => handleStockDelta(grp, +1)}
                  className="flex-1 py-1.5 bg-rose-600 hover:bg-rose-500 text-white rounded-xl flex items-center justify-center shadow-md shadow-rose-600/30 transition-colors"
                  title="Add 1 received unit"
                >
                  <Plus className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
