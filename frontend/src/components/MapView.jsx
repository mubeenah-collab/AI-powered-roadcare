import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { AlertTriangle, ShieldAlert, CheckCircle, Navigation, MapPin } from 'lucide-react';

// Custom Map Marker Icons based on Severity Level
const getSeverityColor = (severity) => {
  switch (severity) {
    case 'Critical': return '#e60000';
    case 'High': return '#ff6600';
    case 'Medium': return '#ffb700';
    default: return '#00cc44';
  }
};

const createCustomIcon = (severity) => {
  const color = getSeverityColor(severity);
  const svgHtml = `
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="16" cy="16" r="12" fill="${color}" fill-opacity="0.25" stroke="${color}" stroke-width="3"/>
      <circle cx="16" cy="16" r="6" fill="${color}"/>
    </svg>
  `;
  return L.divIcon({
    className: 'custom-map-pin',
    html: svgHtml,
    iconSize: [32, 32],
    iconAnchor: [16, 16]
  });
};

export default function MapView({ reports }) {
  const [filterSeverity, setFilterSeverity] = useState('ALL');
  const center = [37.7749, -122.4194]; // Default Map Center (San Francisco / Demo Region)

  const filteredReports = reports.filter(r => {
    if (filterSeverity !== 'ALL' && r.severity !== filterSeverity) return false;
    return true;
  });

  return (
    <div className="relative w-full h-[650px] rounded-xl overflow-hidden shadow-2xl border border-slate-700 bg-slate-900">
      {/* Map Control Bar Overlay */}
      <div className="absolute top-4 right-4 z-[1000] bg-slate-900/90 backdrop-blur-md px-4 py-2 rounded-lg border border-slate-700 shadow-lg flex items-center gap-3 text-sm text-slate-200">
        <span className="font-semibold text-slate-400">Severity Filter:</span>
        {['ALL', 'Critical', 'High', 'Medium', 'Low'].map((sev) => (
          <button
            key={sev}
            onClick={() => setFilterSeverity(sev)}
            className={`px-3 py-1 rounded-md transition-all font-medium text-xs ${
              filterSeverity === sev 
                ? 'bg-blue-600 text-white shadow' 
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            {sev}
          </button>
        ))}
      </div>

      {/* Leaflet Map Component */}
      <MapContainer center={center} zoom={13} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors & Dynamic CartoDB Dark'
          url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
        />

        {filteredReports.map((report) => (
          <React.Fragment key={report.id}>
            {/* Spatial Buffer Circle showing 10m spatial deduplication zone */}
            <Circle 
              center={[report.latitude, report.longitude]} 
              radius={10} 
              pathOptions={{ color: getSeverityColor(report.severity), fillColor: getSeverityColor(report.severity), fillOpacity: 0.15, weight: 1 }}
            />
            
            <Marker 
              position={[report.latitude, report.longitude]} 
              icon={createCustomIcon(report.severity)}
            >
              <Popup className="custom-popup">
                <div className="p-3 max-w-xs text-slate-900 font-sans">
                  <div className="flex items-center justify-between border-b pb-2 mb-2">
                    <span className="font-bold text-sm text-slate-800">{report.damage_type}</span>
                    <span 
                      className="px-2 py-0.5 text-xs font-semibold rounded text-white"
                      style={{ backgroundColor: getSeverityColor(report.severity) }}
                    >
                      {report.severity}
                    </span>
                  </div>
                  
                  <div className="space-y-1 text-xs text-slate-600">
                    <p><strong className="text-slate-800">Priority Score:</strong> {report.priority_score} / 100</p>
                    <p><strong className="text-slate-800">Location:</strong> {report.road_name || 'Main St'}, {report.city}</p>
                    <p><strong className="text-slate-800">Est. Area:</strong> {report.estimated_area_m2 || 0.45} m²</p>
                    {report.estimated_depth_cm && (
                      <p><strong className="text-slate-800">Est. Depth:</strong> {report.estimated_depth_cm} cm</p>
                    )}
                    <p><strong className="text-slate-800">Source:</strong> {report.source_type === 'government_fleet' ? 'Fleet Vehicle' : 'Citizen App'}</p>
                    <p><strong className="text-slate-800">Verifications:</strong> {report.verification_count} merged reports</p>
                  </div>
                  
                  <button className="mt-3 w-full bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold py-1.5 rounded transition">
                    Assign Repair Task
                  </button>
                </div>
              </Popup>
            </Marker>
          </React.Fragment>
        ))}
      </MapContainer>
    </div>
  );
}
