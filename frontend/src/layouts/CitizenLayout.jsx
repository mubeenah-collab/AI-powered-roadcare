import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from '../components/Navbar';

export const CitizenLayout = () => {
  return (
    <div className="min-h-screen flex flex-col bg-[#0F172A]">
      <Navbar />
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
        <Outlet />
      </main>
      <footer className="glass-panel border-t border-slate-800 py-6 text-center text-xs text-slate-400">
        <p>© 2026 RoadVision AI. Smart City MLOps & Municipal Pavement Monitoring Platform.</p>
      </footer>
    </div>
  );
};

export default CitizenLayout;
