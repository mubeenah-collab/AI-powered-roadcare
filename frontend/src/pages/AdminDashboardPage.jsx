import React, { useState, useEffect } from 'react';
import DashboardCard from '../components/DashboardCard';
import MapComponent from '../components/MapComponent';
import { fetchAdminDashboardKPIs, fetchAdminComplaints } from '../services/api';
import { Activity, ShieldAlert, CheckCircle2, Clock, Truck, MapPin } from 'lucide-react';

export const AdminDashboardPage = () => {
  const [kpis, setKpis] = useState(null);
  const [complaints, setComplaints] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [kpiRes, complaintsRes] = await Promise.all([
          fetchAdminDashboardKPIs(),
          fetchAdminComplaints(),
        ]);
        setKpis(kpiRes);
        setComplaints(complaintsRes);
      } catch (err) {
        console.error("Failed to load admin data:", err);
      } finally {
        setIsLoading(false);
      }
    };
    loadData();
  }, []);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-extrabold text-white">Executive Command Dashboard</h1>
        <p className="text-sm text-slate-400 mt-1">
          Municipal pavement damage overview, continuous fleet telematics, and interactive GIS hotspot tracking.
        </p>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <DashboardCard
          title="Total Scanned Roads"
          value={kpis ? `${kpis.total_roads_scanned_km} km` : "1,420 km"}
          subtitle="Greater Chennai Corporation"
          icon={Activity}
          color="blue"
        />
        <DashboardCard
          title="Critical Defects"
          value={kpis ? `${kpis.critical_defects_count}` : "7"}
          subtitle="Requires immediate dispatch"
          icon={ShieldAlert}
          color="red"
        />
        <DashboardCard
          title="Pending Verification"
          value={kpis ? `${kpis.pending_verification}` : "12"}
          subtitle="Awaiting municipal inspector"
          icon={Clock}
          color="amber"
        />
        <DashboardCard
          title="Completed Repairs"
          value={kpis ? `${kpis.completed_repairs}` : "24"}
          subtitle="After-repair verified"
          icon={CheckCircle2}
          color="green"
        />
      </div>

      {/* Interactive Map & Active Transit Fleet Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 glass-panel p-5 rounded-2xl border border-slate-700/60 flex flex-col h-[480px]">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-bold text-white flex items-center space-x-2">
              <MapPin className="w-5 h-5 text-blue-400" />
              <span>Interactive Pavement Hazard Map</span>
            </h2>
            <span className="text-xs font-semibold text-slate-400 bg-slate-800 px-3 py-1 rounded-full border border-slate-700">
              Live GIS OpenStreetMap Tiles
            </span>
          </div>
          <div className="flex-1 rounded-xl overflow-hidden">
            <MapComponent complaints={complaints} />
          </div>
        </div>

        {/* Transit Fleet Surveillance Sidebar */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-700/60 space-y-4">
          <div className="flex items-center space-x-2 text-emerald-400 font-bold text-sm">
            <Truck className="w-5 h-5" />
            <h3>Continuous Fleet Telematics</h3>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            Dashcams mounted on public buses and garbage trucks stream frames every 5 seconds over 4G/5G networks.
          </p>

          <div className="space-y-3 pt-2">
            <div className="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700 space-y-1">
              <div className="flex items-center justify-between text-xs font-bold text-white">
                <span>Vehicle: TN01-GOV-024</span>
                <span className="text-emerald-400">Active</span>
              </div>
              <p className="text-[11px] text-slate-400">Type: Government Bus | Dept: Greater Chennai Corp</p>
              <p className="text-[11px] text-slate-400">Route: Anna Salai Route | Camera: CAM-003</p>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700 space-y-1">
              <div className="flex items-center justify-between text-xs font-bold text-white">
                <span>Vehicle: TN01-GOV-089</span>
                <span className="text-emerald-400">Active</span>
              </div>
              <p className="text-[11px] text-slate-400">Type: Garbage Truck | Dept: Municipal Waste</p>
              <p className="text-[11px] text-slate-400">Route: GST Road Route | Camera: CAM-012</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboardPage;
