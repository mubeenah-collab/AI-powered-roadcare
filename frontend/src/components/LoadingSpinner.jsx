import React from 'react';

export const LoadingSpinner = ({ label = "Processing with RoadVision AI..." }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-4">
      <div className="relative w-12 h-12">
        <div className="absolute inset-0 rounded-full border-4 border-blue-500/20"></div>
        <div className="absolute inset-0 rounded-full border-4 border-blue-500 border-t-transparent animate-spin"></div>
      </div>
      <p className="text-sm font-medium text-slate-300 animate-pulse">{label}</p>
    </div>
  );
};

export default LoadingSpinner;
