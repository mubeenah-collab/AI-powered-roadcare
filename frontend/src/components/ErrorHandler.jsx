import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

export const ErrorHandler = ({ message = "An error occurred while connecting to RoadVision API.", onRetry }) => {
  return (
    <div className="glass-panel p-6 rounded-2xl border-red-500/30 bg-red-500/5 text-center space-y-4 max-w-md mx-auto">
      <div className="w-12 h-12 mx-auto rounded-full bg-red-500/10 flex items-center justify-center text-red-400">
        <AlertTriangle className="w-6 h-6" />
      </div>
      <div>
        <h4 className="text-base font-bold text-white">API Communication Alert</h4>
        <p className="text-xs text-slate-300 mt-1 leading-relaxed">{message}</p>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center space-x-2 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition-colors"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Retry Connection</span>
        </button>
      )}
    </div>
  );
};

export default ErrorHandler;
