import React, { useState, useEffect } from 'react';
import { fetchAdminComplaints, completeRepairTask } from '../services/api';
import { ListFilter, ShieldAlert, Upload, CheckCircle, Eye, X } from 'lucide-react';

export const AdminComplaintsPage = () => {
  const [complaints, setComplaints] = useState([]);
  const [selectedComplaint, setSelectedComplaint] = useState(null);
  const [afterImageInput, setAfterImageInput] = useState('https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&w=800&q=80');
  const [officerName, setOfficerName] = useState('Chief Engineer R. Sundaram');
  const [comments, setComments] = useState('Resurfacing completed with high-durability asphalt patch.');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    const loadComplaints = async () => {
      const data = await fetchAdminComplaints();
      setComplaints(data);
    };
    loadComplaints();
  }, []);

  const handleCompleteRepair = async (e) => {
    e.preventDefault();
    if (!selectedComplaint) return;

    setIsSubmitting(true);
    try {
      await completeRepairTask(selectedComplaint.complaint_id, afterImageInput, officerName, comments);
      
      // Update local state
      setComplaints((prev) =>
        prev.map((c) =>
          c.complaint_id === selectedComplaint.complaint_id
            ? { ...c, status: 'Completed', after_image_url: afterImageInput }
            : c
        )
      );
      setSelectedComplaint(null);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-extrabold text-white">Complaint & Workorder Dispatching Table</h1>
        <p className="text-sm text-slate-400 mt-1">
          Review, assign paving contractors, and upload after-repair verification photos for 8-stage lifecycle tracking.
        </p>
      </div>

      {/* DataTable Container */}
      <div className="glass-panel rounded-2xl border border-slate-700/60 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-800/80 text-slate-300 uppercase font-semibold border-b border-slate-700">
              <tr>
                <th className="px-4 py-3.5">Complaint ID</th>
                <th className="px-4 py-3.5">Original Image</th>
                <th className="px-4 py-3.5">Damage Type</th>
                <th className="px-4 py-3.5">Severity</th>
                <th className="px-4 py-3.5">Location</th>
                <th className="px-4 py-3.5">Priority</th>
                <th className="px-4 py-3.5">Status</th>
                <th className="px-4 py-3.5 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/50 text-slate-200">
              {complaints.map((item, idx) => {
                const loc = item.location || {};
                return (
                  <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                    <td className="px-4 py-3.5 font-bold text-blue-400 font-mono">{item.complaint_id}</td>
                    <td className="px-4 py-3.5">
                      <div className="w-12 h-12 rounded-lg overflow-hidden border border-slate-700">
                        <img
                          src={item.before_image_url || "https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?auto=format&fit=crop&w=800&q=80"}
                          alt="Road Defect"
                          className="w-full h-full object-cover"
                        />
                      </div>
                    </td>
                    <td className="px-4 py-3.5 font-semibold text-white">{item.damage_type}</td>
                    <td className="px-4 py-3.5">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        item.severity === 'Critical' ? 'bg-red-500/20 text-red-400 border border-red-500/30' : 'bg-orange-500/20 text-orange-400 border border-orange-500/30'
                      }`}>
                        {item.severity}
                      </span>
                    </td>
                    <td className="px-4 py-3.5 text-slate-300">
                      {loc.road_name || 'Anna Salai'}, {loc.area || 'Teynampet'}
                    </td>
                    <td className="px-4 py-3.5 font-bold text-amber-400">{item.priority_score || 89}</td>
                    <td className="px-4 py-3.5">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                        item.status === 'Completed' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-blue-500/20 text-blue-400'
                      }`}>
                        {item.status}
                      </span>
                    </td>
                    <td className="px-4 py-3.5 text-right">
                      {item.status !== 'Completed' ? (
                        <button
                          onClick={() => setSelectedComplaint(item)}
                          className="px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs shadow-md transition-all inline-flex items-center space-x-1"
                        >
                          <Upload className="w-3.5 h-3.5" />
                          <span>Verify Repair</span>
                        </button>
                      ) : (
                        <span className="text-emerald-400 font-semibold text-[11px] inline-flex items-center space-x-1">
                          <CheckCircle className="w-3.5 h-3.5" />
                          <span>Verified</span>
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Repair Verification Modal */}
      {selectedComplaint && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
          <div className="glass-panel max-w-lg w-full rounded-2xl p-6 border border-slate-700 space-y-5 animate-fadeIn">
            <div className="flex items-center justify-between pb-3 border-b border-slate-700">
              <h3 className="text-base font-bold text-white">After-Repair Photo Verification</h3>
              <button onClick={() => setSelectedComplaint(null)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCompleteRepair} className="space-y-4 text-xs">
              <div>
                <label className="text-slate-300 font-semibold">Complaint ID</label>
                <input
                  type="text"
                  disabled
                  value={selectedComplaint.complaint_id}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white font-mono mt-1"
                />
              </div>

              <div>
                <label className="text-slate-300 font-semibold">After-Repair Resurfaced Photo URL</label>
                <input
                  type="text"
                  value={afterImageInput}
                  onChange={(e) => setAfterImageInput(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white mt-1 focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="text-slate-300 font-semibold">Verifying Chief Engineer</label>
                <input
                  type="text"
                  value={officerName}
                  onChange={(e) => setOfficerName(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white mt-1"
                />
              </div>

              <div>
                <label className="text-slate-300 font-semibold">Inspection Notes</label>
                <textarea
                  rows={3}
                  value={comments}
                  onChange={(e) => setComments(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white mt-1 focus:outline-none focus:border-blue-500"
                ></textarea>
              </div>

              <div className="flex justify-end space-x-3 pt-2">
                <button
                  type="button"
                  onClick={() => setSelectedComplaint(null)}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 hover:bg-slate-700 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold shadow-lg shadow-emerald-600/30"
                >
                  {isSubmitting ? 'Saving...' : 'Mark Completed'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminComplaintsPage;
