import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, Legend
} from 'recharts';
import { BarChart3, TrendingUp, PieChart as PieIcon, Activity } from 'lucide-react';

const damageDistributionData = [
  { name: 'Pothole', count: 48, fill: '#EF4444' },
  { name: 'Alligator Crack', count: 32, fill: '#F97316' },
  { name: 'Longitudinal Crack', count: 24, fill: '#3B82F6' },
  { name: 'Transverse Crack', count: 18, fill: '#10B981' },
  { name: 'Surface Damage', count: 14, fill: '#8B5CF6' },
];

const monthlyTrendData = [
  { month: 'Jan', citizen: 18, fleet: 34 },
  { month: 'Feb', citizen: 24, fleet: 42 },
  { month: 'Mar', citizen: 31, fleet: 56 },
  { month: 'Apr', citizen: 28, fleet: 62 },
  { month: 'May', citizen: 42, fleet: 78 },
  { month: 'Jun', citizen: 45, fleet: 79 },
];

const severityData = [
  { name: 'Critical', value: 15, color: '#EF4444' },
  { name: 'High', value: 35, color: '#F97316' },
  { name: 'Medium', value: 30, color: '#3B82F6' },
  { name: 'Low', value: 20, color: '#10B981' },
];

export const AdminAnalyticsPage = () => {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-extrabold text-white">Advanced Analytics & Machine Learning Visualizer</h1>
        <p className="text-sm text-slate-400 mt-1">
          Quantitative statistics on pavement defect frequency, monthly ingestion trends, and spatial severity distributions.
        </p>
      </div>

      {/* Top 2 Chart Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Damage Distribution Bar Chart */}
        <div className="glass-panel p-6 rounded-2xl border border-slate-700/60 space-y-4">
          <h2 className="text-base font-bold text-white flex items-center space-x-2">
            <BarChart3 className="w-5 h-5 text-blue-400" />
            <span>Damage Type Distribution</span>
          </h2>
          <div className="h-72 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={damageDistributionData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" stroke="#94A3B8" fontSize={11} />
                <YAxis stroke="#94A3B8" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#334155', borderRadius: '12px' }} />
                <Bar dataKey="count" radius={[8, 8, 0, 0]}>
                  {damageDistributionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Ingestion Stream Trend Line Chart */}
        <div className="glass-panel p-6 rounded-2xl border border-slate-700/60 space-y-4">
          <h2 className="text-base font-bold text-white flex items-center space-x-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            <span>Monthly Ingestion Channels (Citizen vs Fleet)</span>
          </h2>
          <div className="h-72 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={monthlyTrendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="month" stroke="#94A3B8" fontSize={11} />
                <YAxis stroke="#94A3B8" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#334155', borderRadius: '12px' }} />
                <Legend />
                <Line type="monotone" dataKey="fleet" stroke="#10B981" strokeWidth={3} name="Government Fleet Telematics" />
                <Line type="monotone" dataKey="citizen" stroke="#3B82F6" strokeWidth={3} name="Citizen Mobile Reports" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Bottom Chart Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Severity Pie Chart */}
        <div className="glass-panel p-6 rounded-2xl border border-slate-700/60 space-y-4">
          <h2 className="text-base font-bold text-white flex items-center space-x-2">
            <PieIcon className="w-5 h-5 text-amber-400" />
            <span>Severity Level Breakdown</span>
          </h2>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={severityData} cx="50%" cy="50%" innerRadius={55} outerRadius={80} paddingAngle={5} dataKey="value">
                  {severityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#334155', borderRadius: '12px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Statistical Summary Box */}
        <div className="lg:col-span-2 glass-panel p-6 rounded-2xl border border-slate-700/60 space-y-4 flex flex-col justify-between">
          <h2 className="text-base font-bold text-white flex items-center space-x-2">
            <Activity className="w-5 h-5 text-purple-400" />
            <span>Municipal Pavement Health Summary</span>
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 text-xs">
            <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-700">
              <span className="text-slate-400">Average Pavement Health</span>
              <p className="text-xl font-bold text-emerald-400 mt-1">72.8 %</p>
            </div>
            <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-700">
              <span className="text-slate-400">Average AI Accuracy</span>
              <p className="text-xl font-bold text-blue-400 mt-1">96.4 %</p>
            </div>
            <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-700">
              <span className="text-slate-400">Most Dangerous Zone</span>
              <p className="text-sm font-bold text-white mt-1">Anna Salai, Chennai</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminAnalyticsPage;
