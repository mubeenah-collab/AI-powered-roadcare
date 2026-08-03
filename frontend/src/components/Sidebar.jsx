import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, BarChart3, ListFilter, MapPin, Truck, ShieldCheck, Settings } from 'lucide-react';

export const Sidebar = () => {
  const links = [
    { to: '/admin', label: 'Executive Dashboard', icon: LayoutDashboard, exact: true },
    { to: '/admin/analytics', label: 'Advanced Analytics', icon: BarChart3 },
    { to: '/admin/complaints', label: 'Complaint Dispatch', icon: ListFilter },
  ];

  return (
    <aside className="w-64 glass-panel min-h-[calc(100vh-4rem)] border-r border-slate-700/60 p-4 flex flex-col justify-between">
      <div className="space-y-6">
        <div>
          <h2 className="px-3 text-xs font-bold uppercase tracking-wider text-slate-400">
            Municipal Command
          </h2>
          <div className="mt-3 space-y-1">
            {links.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.exact}
                  className={({ isActive }) =>
                    `flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                      isActive
                        ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                    }`
                  }
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </div>
        </div>

        {/* Government Fleet Sub-Section */}
        <div>
          <h2 className="px-3 text-xs font-bold uppercase tracking-wider text-slate-400">
            Fleet Telematics
          </h2>
          <div className="mt-3 p-3 rounded-xl bg-slate-800/40 border border-slate-700/50 space-y-2">
            <div className="flex items-center space-x-2 text-xs font-semibold text-emerald-400">
              <Truck className="w-4 h-4" />
              <span>Active Transit Fleet</span>
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Continuous dashcam streams: <strong className="text-white">TN01-GOV-024</strong> (Greater Chennai Corp).
            </p>
          </div>
        </div>
      </div>

      {/* Footer Meta */}
      <div className="pt-4 border-t border-slate-700/60 text-xs text-slate-400">
        <div className="flex items-center justify-between">
          <span>Engine Status</span>
          <span className="flex items-center space-x-1 text-emerald-400 font-semibold">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>Online</span>
          </span>
        </div>
        <p className="mt-1 text-[10px] text-slate-400">YOLOv11 + PostGIS Spatial 3.3</p>
      </div>
    </aside>
  );
};

export default Sidebar;
