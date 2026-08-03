import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

// Custom Marker Icons for Leaflet
const createCustomIcon = (severity) => {
  const color = severity === 'Critical' ? '#EF4444' : severity === 'High' ? '#F97316' : '#3B82F6';
  return L.divIcon({
    className: 'custom-leaflet-marker',
    html: `
      <div style="
        background-color: ${color};
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: 3px solid #0F172A;
        box-shadow: 0 0 10px ${color};
      "></div>
    `,
    iconSize: [24, 24],
    iconAnchor: [12, 12],
  });
};

export const MapComponent = ({ complaints = [], center = [12.926543, 80.143287], zoom = 12 }) => {
  return (
    <div className="w-full h-full min-h-[380px] rounded-2xl overflow-hidden border border-slate-700/60 shadow-xl relative z-0">
      <MapContainer center={center} zoom={zoom} scrollWheelZoom={false} className="w-full h-full min-h-[380px]">
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {complaints.map((item, idx) => {
          const lat = item.coordinates?.latitude || 12.926543;
          const lng = item.coordinates?.longitude || 80.143287;
          const loc = item.location || {};
          return (
            <Marker key={idx} position={[lat, lng]} icon={createCustomIcon(item.severity)}>
              <Popup>
                <div className="p-1 max-w-xs text-slate-900">
                  <div className="flex items-center justify-between font-bold text-sm">
                    <span>{item.damage_type || 'Pothole'}</span>
                    <span className="px-2 py-0.5 text-[10px] rounded bg-red-100 text-red-700 font-semibold">{item.severity}</span>
                  </div>
                  <p className="text-xs text-slate-600 mt-1 font-semibold">
                    {loc.road_name || 'Anna Salai'}, {loc.area || 'Teynampet'}, {loc.city || 'Chennai'}
                  </p>
                  <div className="mt-2 pt-2 border-t border-slate-200 text-[11px] text-slate-500">
                    <div>Priority Score: <strong>{item.priority_score || 89} / 100</strong></div>
                    <div>Status: <strong className="text-blue-600">{item.status || 'Pending Verification'}</strong></div>
                  </div>
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
};

export default MapComponent;
