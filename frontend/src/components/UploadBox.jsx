import React, { useState, useRef } from 'react';
import { UploadCloud, Image as ImageIcon, CheckCircle, AlertCircle, RefreshCw } from 'lucide-react';

export const UploadBox = ({ onImageSelected, isAnalyzing, selectedFile }) => {
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onImageSelected(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      onImageSelected(e.target.files[0]);
    }
  };

  return (
    <div className="w-full">
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleChange}
        className="hidden"
      />

      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all ${
          dragActive
            ? 'border-blue-500 bg-blue-500/10'
            : selectedFile
            ? 'border-emerald-500/50 bg-slate-800/60'
            : 'border-slate-700 bg-slate-800/40 hover:border-slate-500 hover:bg-slate-800/60'
        }`}
      >
        {selectedFile ? (
          <div className="space-y-4">
            <div className="relative mx-auto max-w-xs h-48 rounded-xl overflow-hidden shadow-lg border border-slate-700">
              <img
                src={URL.createObjectURL(selectedFile)}
                alt="Selected Road Surface"
                className="w-full h-full object-cover"
              />
            </div>
            <div className="flex items-center justify-center space-x-2 text-emerald-400 text-sm font-semibold">
              <CheckCircle className="w-4 h-4" />
              <span>{selectedFile.name} ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)</span>
            </div>
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                fileInputRef.current?.click();
              }}
              className="inline-flex items-center space-x-1.5 text-xs text-slate-400 hover:text-white bg-slate-700/60 px-3 py-1.5 rounded-lg border border-slate-600"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Change Image</span>
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            <div className="w-16 h-16 mx-auto rounded-2xl bg-blue-600/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
              <UploadCloud className="w-8 h-8" />
            </div>
            <div>
              <p className="text-base font-semibold text-white">
                Drop pavement image here, or <span className="text-blue-400 underline">browse</span>
              </p>
              <p className="text-xs text-slate-400 mt-1">Supports JPG, PNG, WEBP (Max 15MB)</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadBox;
