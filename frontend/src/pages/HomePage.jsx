import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldAlert, Camera, Truck, Activity, ArrowRight, CheckCircle2 } from 'lucide-react';
import DashboardCard from '../components/DashboardCard';

export const HomePage = () => {
  return (
    <div className="space-y-16 py-6">
      {/* Hero Section */}
      <section className="relative glass-panel rounded-3xl p-8 sm:p-12 overflow-hidden border border-slate-700/60">
        <div className="absolute top-0 right-0 -mt-12 -mr-12 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>
        
        <div className="max-w-3xl relative z-10 space-y-6">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold">
            <span className="w-2 h-2 rounded-full bg-blue-400 animate-ping"></span>
            <span>AI-Powered Smart City Infrastructure</span>
          </div>

          <h1 className="text-4xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight">
            Intelligent Road Damage Detection & Monitoring Platform
          </h1>

          <p className="text-base text-slate-300 leading-relaxed">
            Automating pavement inspection through crowdsourced citizen mobile reporting and continuous municipal fleet dashcam surveillance. Powered by YOLOv11 Computer Vision, MiDaS 3D Monocular Depth, and PostGIS Spatial GIS.
          </p>

          <div className="flex flex-wrap gap-4 pt-2">
            <Link
              to="/report"
              className="inline-flex items-center space-x-2 px-6 py-3.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold shadow-lg shadow-blue-600/30 transition-all hover:scale-105"
            >
              <Camera className="w-5 h-5" />
              <span>Report Road Hazard</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
            <Link
              to="/track"
              className="inline-flex items-center space-x-2 px-6 py-3.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold border border-slate-700 transition-all"
            >
              <span>Track Existing Complaint</span>
            </Link>
          </div>
        </div>
      </section>

      {/* KPI Stats Overview Grid */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <DashboardCard
          title="Scanned Kilometers"
          value="1,420 km"
          subtitle="Greater Chennai Corp"
          icon={Activity}
          color="blue"
          trend="+12.4%"
        />
        <DashboardCard
          title="AI Detection Accuracy"
          value="96.4%"
          subtitle="YOLOv11 + MiDaS 3D"
          icon={ShieldAlert}
          color="green"
          trend="Validated"
        />
        <DashboardCard
          title="Active Fleet Vehicles"
          value="79 Bus & Trucks"
          subtitle="Continuous telematics"
          icon={Truck}
          color="purple"
        />
        <DashboardCard
          title="Avg Repair SLA"
          value="2.4 Days"
          subtitle="Target: 3.0 Days"
          icon={CheckCircle2}
          color="amber"
          trend="-18% SLA"
        />
      </section>
    </div>
  );
};

export default HomePage;
