import React, { useState, useEffect } from 'react';
import MapView from './components/MapView';
import { 
  ShieldAlert, 
  Map, 
  BarChart3, 
  Truck, 
  FileText, 
  RefreshCw, 
  Layers, 
  CheckCircle,
  AlertTriangle,
  Activity
} from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('map');
  const [stats, setStats] = useState({
    total_complaints: 48,
    critical: 7,
    high: 14,
    medium: 18,
    low: 9,
    pending_repairs: 36,
    completed_repairs: 12,
    citizen_reports: 22,
    government_reports: 26
  });

  const [reports, setReports] = useState([
    {
      id: 'r-101',
      damage_type: 'Pothole',
      severity: 'Critical',
      priority_score: 92.4,
      latitude: 37.7749,
      longitude: -122.4194,
      road_name: 'Market Street',
      city: 'San Francisco',
      estimated_area_m2: 1.25,
      estimated_depth_cm: 9.8,
      source_type: 'government_fleet',
      verification_count: 5,
      status: 'pending'
    },
    {
      id: 'r-102',
      damage_type: 'Alligator Crack',
      severity: 'High',
      priority_score: 74.2,
      latitude: 37.7833,
      longitude: -122.4167,
      road_name: 'Van Ness Avenue',
      city: 'San Francisco',
      estimated_area_m2: 3.40,
      estimated_depth_cm: 3.2,
      source_type: 'citizen',
      verification_count: 2,
      status: 'assigned'
    },
    {
      id: 'r-103',
      damage_type: 'Longitudinal Crack',
      severity: 'Medium',
      priority_score: 48.0,
      latitude: 37.7690,
      longitude: -122.4480,
      road_name: 'Haight Street',
      city: 'San Francisco',
      estimated_area_m2: 0.85,
      estimated_depth_cm: 1.5,
      source_type: 'government_fleet',
      verification_count: 1,
      status: 'pending'
    }
  ]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans flex flex-col">
      {/* Top Header Navbar */}
      <header className="bg-slate-900/90 backdrop-blur-md border-b border-slate-800 px-6 py-4 flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-lg shadow-lg">
            <Activity className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-blue-400">
              RoadVision AI
            </h1>
            <p className="text-xs text-slate-400">Intelligent Road Damage Monitoring Ecosystem</p>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex bg-slate-800/80 p-1 rounded-xl border border-slate-700">
          <button
            onClick={() => setActiveTab('map')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition ${
              activeTab === 'map' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Map className="w-4 h-4" /> GIS Map View
          </button>
          <button
            onClick={() => setActiveTab('complaints')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition ${
              activeTab === 'complaints' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <FileText className="w-4 h-4" /> Complaint Registry
          </button>
          <button
            onClick={() => setActiveTab('fleet')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition ${
              activeTab === 'fleet' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Truck className="w-4 h-4" /> Fleet Tracker
          </button>
        </div>

        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300 rounded-lg border border-slate-700 transition">
            <RefreshCw className="w-3.5 h-3.5" /> Live Sync
          </button>
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 p-6 max-w-7xl w-full mx-auto space-y-6">
        {/* KPI Summary Cards Bar */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-400 font-medium">Total Defects Logged</p>
              <h3 className="text-2xl font-bold text-white mt-1">{stats.total_complaints}</h3>
            </div>
            <div className="p-3 bg-blue-500/10 rounded-lg text-blue-400">
              <Layers className="w-6 h-6" />
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-400 font-medium">Critical / High Hazard</p>
              <h3 className="text-2xl font-bold text-red-400 mt-1">{stats.critical + stats.high}</h3>
            </div>
            <div className="p-3 bg-red-500/10 rounded-lg text-red-400">
              <ShieldAlert className="w-6 h-6" />
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-400 font-medium">Pending Repairs</p>
              <h3 className="text-2xl font-bold text-amber-400 mt-1">{stats.pending_repairs}</h3>
            </div>
            <div className="p-3 bg-amber-500/10 rounded-lg text-amber-400">
              <AlertTriangle className="w-6 h-6" />
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-400 font-medium">Govt Fleet Monitoring</p>
              <h3 className="text-2xl font-bold text-emerald-400 mt-1">{stats.government_reports} Reports</h3>
            </div>
            <div className="p-3 bg-emerald-500/10 rounded-lg text-emerald-400">
              <Truck className="w-6 h-6" />
            </div>
          </div>
        </div>

        {/* Tab Body Content */}
        {activeTab === 'map' && (
          <div className="space-y-4">
            <h2 className="text-lg font-bold text-slate-200">Municipal GIS Road Damage Heatmap & Inspection Pins</h2>
            <MapView reports={reports} />
          </div>
        )}

        {activeTab === 'complaints' && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <h2 className="text-lg font-bold text-slate-200">Active Damage Complaint Registry</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-800 text-slate-400 uppercase">
                  <tr>
                    <th className="p-3">Defect ID</th>
                    <th className="p-3">Damage Type</th>
                    <th className="p-3">Severity</th>
                    <th className="p-3">Priority Score</th>
                    <th className="p-3">Location / Road</th>
                    <th className="p-3">Est. Depth</th>
                    <th className="p-3">Source</th>
                    <th className="p-3">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {reports.map((r) => (
                    <tr key={r.id} className="hover:bg-slate-800/50 transition">
                      <td className="p-3 font-mono text-blue-400">{r.id}</td>
                      <td className="p-3 font-semibold text-white">{r.damage_type}</td>
                      <td className="p-3">
                        <span className={`px-2 py-1 rounded font-bold text-[10px] ${
                          r.severity === 'Critical' ? 'bg-red-500/20 text-red-400 border border-red-500/40' :
                          r.severity === 'High' ? 'bg-orange-500/20 text-orange-400 border border-orange-500/40' : 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/40'
                        }`}>
                          {r.severity}
                        </span>
                      </td>
                      <td className="p-3 font-bold text-slate-200">{r.priority_score} / 100</td>
                      <td className="p-3">{r.road_name}, {r.city}</td>
                      <td className="p-3">{r.estimated_depth_cm} cm</td>
                      <td className="p-3 capitalize">{r.source_type.replace('_', ' ')}</td>
                      <td className="p-3">
                        <button className="px-3 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded font-medium text-xs transition">
                          Dispatch Maintenance
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'fleet' && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-center py-16 text-slate-400">
            <Truck className="w-12 h-12 text-blue-500 mx-auto mb-3 animate-pulse" />
            <h3 className="text-lg font-bold text-white">Government Fleet Continuous Monitoring Active</h3>
            <p className="text-xs text-slate-400 max-w-md mx-auto mt-1">
              Garbage trucks, municipal buses, and highway inspection vehicles are transmitting automated 4G/5G road camera frames.
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
