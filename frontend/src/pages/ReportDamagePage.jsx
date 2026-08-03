import React, { useState } from 'react';
import UploadBox from '../components/UploadBox';
import MapComponent from '../components/MapComponent';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorHandler from '../components/ErrorHandler';
import { uploadRoadDamageImage } from '../services/api';
import { ShieldCheck, MapPin, Sun, CloudRain, AlertTriangle, Send } from 'lucide-react';

export const ReportDamagePage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [aiResult, setAiResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [submittedSuccess, setSubmittedSuccess] = useState(false);

  const [locationLat, setLocationLat] = useState(12.926543);
  const [locationLng, setLocationLng] = useState(80.143287);

  const handleImageSelected = (file) => {
    setSelectedFile(file);
    setAiResult(null);
    setErrorMessage(null);
    setSubmittedSuccess(false);
  };

  const handleAnalyzeAndSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    setIsAnalyzing(true);
    setErrorMessage(null);

    try {
      const res = await uploadRoadDamageImage(selectedFile, locationLat, locationLng, 'Citizen');
      setAiResult(res);
    } catch (err) {
      setErrorMessage(err.message || 'Inspection failed.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getConfidenceColor = (conf) => {
    if (conf >= 0.90) return 'text-emerald-400';
    if (conf >= 0.70) return 'text-amber-400';
    return 'text-red-400';
  };

  const buildConfidenceBar = (conf) => {
    const filled = Math.round(conf * 10);
    const empty = 10 - filled;
    return '█'.repeat(filled) + '░'.repeat(empty) + ` ${(conf * 100).toFixed(1)}%`;
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 py-4">
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white">Report Road Surface Hazard</h1>
        <p className="text-sm text-slate-400 mt-1">
          Upload pavement photo. Location and AI metric analysis are computed automatically.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Form Column */}
        <form onSubmit={handleAnalyzeAndSubmit} className="space-y-6">
          <div className="glass-panel p-6 rounded-2xl space-y-6 border border-slate-700/60">
            <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300">1. Pavement Photo Upload</h2>
            <UploadBox
              onImageSelected={handleImageSelected}
              isAnalyzing={isAnalyzing}
              selectedFile={selectedFile}
            />

            <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300 pt-2">2. Detected GPS Coordinates</h2>
            <div className="p-4 rounded-xl bg-slate-800/60 border border-slate-700 flex items-center space-x-3">
              <MapPin className="w-5 h-5 text-blue-400 flex-shrink-0" />
              <div>
                <p className="text-xs text-slate-400">Indian Address Resolution</p>
                <p className="text-xs font-semibold text-white mt-0.5">
                  Anna Salai, Teynampet, Chennai, Tamil Nadu (600018)
                </p>
              </div>
            </div>

            <button
              type="submit"
              disabled={!selectedFile || isAnalyzing}
              className={`w-full py-3.5 px-6 rounded-xl text-sm font-bold flex items-center justify-center space-x-2 transition-all ${
                !selectedFile || isAnalyzing
                  ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-600/30'
              }`}
            >
              <Send className="w-4 h-4" />
              <span>{isAnalyzing ? 'Running YOLOv11 & MiDaS...' : 'Submit & Analyze Damage'}</span>
            </button>
          </div>
        </form>

        {/* Right Output Column */}
        <div className="space-y-6">
          {isAnalyzing && <LoadingSpinner label="Decoding RGB Image & Estimating 3D Depth Map..." />}

          {errorMessage && <ErrorHandler message={errorMessage} />}

          {aiResult && !isAnalyzing && (
            <div className="glass-panel p-6 rounded-2xl border border-blue-500/40 space-y-5 animate-fadeIn">
              <div className="flex items-center justify-between pb-3 border-b border-slate-700">
                <div className="flex items-center space-x-2">
                  <ShieldCheck className="w-5 h-5 text-emerald-400" />
                  <h3 className="text-base font-bold text-white">AI Diagnosis Successful</h3>
                </div>
                <span className="px-2.5 py-1 text-xs font-bold bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full">
                  {aiResult.complaint_id}
                </span>
              </div>

              {/* Diagnostic Grid */}
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-700/60">
                  <span className="text-slate-400">Defect Class</span>
                  <p className="text-sm font-bold text-white mt-1">{aiResult.damage_type}</p>
                </div>
                <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-700/60">
                  <span className="text-slate-400">Severity Level</span>
                  <p className="text-sm font-bold text-red-400 mt-1">{aiResult.severity}</p>
                </div>
                <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-700/60">
                  <span className="text-slate-400">Priority Score</span>
                  <p className="text-sm font-bold text-amber-400 mt-1">{aiResult.priority_score} / 100</p>
                </div>
                <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-700/60">
                  <span className="text-slate-400">Est. Depth</span>
                  <p className="text-sm font-bold text-white mt-1">{aiResult.estimated_depth_cm} cm</p>
                </div>
              </div>

              {/* AI Confidence Bar */}
              <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-700/60 flex items-center justify-between text-xs font-mono">
                <span className="text-slate-400">AI Confidence Bar</span>
                <span className={`font-bold ${getConfidenceColor(aiResult.confidence)}`}>
                  {buildConfidenceBar(aiResult.confidence)}
                </span>
              </div>

              {/* Live Weather Impact */}
              {aiResult.weather && (
                <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-700 text-xs space-y-1.5">
                  <div className="flex items-center space-x-2 text-amber-400 font-semibold">
                    <CloudRain className="w-4 h-4" />
                    <span>Live Weather Hazard Assessment</span>
                  </div>
                  <p className="text-slate-300">
                    Condition: {aiResult.weather.condition} | Temp: {aiResult.weather.temperature_c}°C | Humidity: {aiResult.weather.humidity_pct}%
                  </p>
                  <p className="text-red-400 font-semibold">
                    Rain Risk: {aiResult.weather.weather_risk} (+15 pt Priority Boost Applied)
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Interactive Location Map */}
          <div className="h-64">
            <MapComponent
              center={[locationLat, locationLng]}
              complaints={aiResult ? [aiResult] : []}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReportDamagePage;
