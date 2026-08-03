import React, { useState } from 'react';
import StatusTimeline from '../components/StatusTimeline';
import { Search, ShieldAlert, MapPin, Calendar, CheckCircle } from 'lucide-react';

export const TrackComplaintPage = () => {
  const [complaintIdInput, setComplaintIdInput] = useState('RV-2026-001245');
  const [activeReport, setActiveReport] = useState({
    complaint_id: "RV-2026-001245",
    source: "Citizen",
    damage_type: "Pothole",
    confidence: 0.964,
    severity: "High",
    priority_score: 89,
    estimated_width_m: 0.82,
    estimated_length_m: 1.05,
    estimated_depth_cm: 8.7,
    status: "Pending Verification",
    location: {
      road_name: "Anna Salai",
      area: "Teynampet",
      city: "Chennai",
      formatted_address: "Anna Salai, Teynampet, Chennai, Tamil Nadu"
    },
    weather: { condition: "Rainy", temperature_c: 31.0, weather_risk: "High" },
    before_image_url: "https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?auto=format&fit=crop&w=800&q=80"
  });

  const handleSearch = (e) => {
    e.preventDefault();
    // Keeps active report loaded for tracking demonstration
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 py-4">
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white">Track Complaint Status</h1>
        <p className="text-sm text-slate-400 mt-1">
          Enter your Complaint ID to track municipal repair dispatch and visual verification timeline.
        </p>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="flex gap-3">
        <div className="relative flex-1">
          <Search className="w-5 h-5 text-slate-400 absolute left-4 top-3.5" />
          <input
            type="text"
            value={complaintIdInput}
            onChange={(e) => setComplaintIdInput(e.target.value)}
            placeholder="Enter Complaint ID (e.g. RV-2026-001245)"
            className="w-full bg-slate-800/80 border border-slate-700 rounded-xl pl-11 pr-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
          />
        </div>
        <button
          type="submit"
          className="px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-sm transition-all"
        >
          Track Status
        </button>
      </form>

      {/* Complaint Status & Timeline Content */}
      {activeReport && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Summary Details */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-700/60 space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-slate-700">
              <span className="text-xs font-semibold text-slate-400">Complaint ID</span>
              <span className="text-sm font-bold text-blue-400">{activeReport.complaint_id}</span>
            </div>

            <div className="space-y-3 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-400">Damage Classification:</span>
                <span className="font-bold text-white">{activeReport.damage_type}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Severity:</span>
                <span className="font-bold text-red-400">{activeReport.severity}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Priority Score:</span>
                <span className="font-bold text-amber-400">{activeReport.priority_score} / 100</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Estimated Depth:</span>
                <span className="font-bold text-white">{activeReport.estimated_depth_cm} cm</span>
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-800/40 border border-slate-700 text-xs">
              <span className="text-slate-400">Pavement Location:</span>
              <p className="font-bold text-white mt-0.5">{activeReport.location?.formatted_address}</p>
            </div>

            {activeReport.before_image_url && (
              <div>
                <span className="text-xs font-semibold text-slate-400">Original Uploaded Image</span>
                <div className="mt-2 h-44 rounded-xl overflow-hidden border border-slate-700">
                  <img src={activeReport.before_image_url} alt="Original Damage" className="w-full h-full object-cover" />
                </div>
              </div>
            )}
          </div>

          {/* Timeline View */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-700/60">
            <StatusTimeline />
          </div>
        </div>
      )}
    </div>
  );
};

export default TrackComplaintPage;
