import React from 'react';
import { CheckCircle2, Circle, Clock, ShieldCheck, UserCheck, Wrench, FileCheck2 } from 'lucide-react';

export const StatusTimeline = ({ timeline = [] }) => {
  const steps = [
    { title: "Submitted", desc: "Citizen uploaded complaint", icon: Clock },
    { title: "AI Verified", desc: "YOLOv11 & MiDaS estimated metrics", icon: ShieldCheck },
    { title: "Assigned", desc: "Municipal contractor assigned", icon: UserCheck },
    { title: "Repair Started", desc: "Resurfacing crew on site", icon: Wrench },
    { title: "Completed", desc: "After-repair photo verified", icon: FileCheck2 },
  ];

  return (
    <div className="space-y-6">
      <h3 className="text-base font-bold text-white flex items-center space-x-2">
        <Clock className="w-5 h-5 text-blue-400" />
        <span>8-Stage Repair Lifecycle Progress</span>
      </h3>

      <div className="relative pl-6 space-y-8 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-700">
        {steps.map((step, idx) => {
          const isDone = idx < 3; // First 3 completed
          const isCurrent = idx === 2;
          const Icon = step.icon;

          return (
            <div key={idx} className="relative flex items-start space-x-4 group">
              <div
                className={`absolute -left-6 top-0.5 w-6 h-6 rounded-full flex items-center justify-center text-xs ring-4 ring-[#0F172A] ${
                  isDone
                    ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/20'
                    : isCurrent
                    ? 'bg-blue-500 text-white animate-pulse'
                    : 'bg-slate-800 text-slate-500 border border-slate-700'
                }`}
              >
                {isDone ? <CheckCircle2 className="w-3.5 h-3.5" /> : <Circle className="w-3 h-3" />}
              </div>

              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <h4 className={`text-sm font-semibold ${isDone ? 'text-white' : 'text-slate-400'}`}>
                    {step.title}
                  </h4>
                  <span className="text-[11px] text-slate-500 font-mono">03 Aug 2026</span>
                </div>
                <p className="text-xs text-slate-400 mt-0.5">{step.desc}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default StatusTimeline;
