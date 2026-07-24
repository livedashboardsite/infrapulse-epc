import { useState, useRef } from 'react';
import { CheckCircle, XCircle, Upload, FileText } from 'lucide-react';

export default function SpecComplianceTab() {
  const [submittal, setSubmittal] = useState({
    submittal_name: 'UPS-01 Submittal',
    battery_runtime_minutes: 22,
    redundancy: 'N+2',
    ups_efficiency_percent: 94.5,
    chiller_n_plus_1: true
  });
  const [result, setResult] = useState(null);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [mode, setMode] = useState('form');
  const fileInputRef = useRef(null);

  const handleCheck = async () => {
    const response = await fetch('/api/spec-compliance/check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(submittal)
    });
    const data = await response.json();
    setResult(data);
  };

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleFileUpload = async () => {
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/spec-compliance/upload', {
      method: 'POST',
      body: formData
    });
    const data = await response.json();
    setResult(data);
    setUploading(false);
  };

  return (
    <div className="space-y-6">
      <div className="liquid-panel p-6">
        <h2 className="text-2xl font-bold mb-6" style={{ color: 'var(--text-primary)' }}>
          Specification & Quality Compliance Agent
          <span className="ml-3 text-sm font-normal px-3 py-1 rounded-full bg-gradient-to-r from-violet-600/20 to-cyan-500/20 text-cyan-400">
            Antigravity Agent Active
          </span>
        </h2>

        <div className="flex gap-4 mb-6">
          <button
            onClick={() => { setMode('form'); setResult(null); }}
            className={`px-6 py-2 rounded-xl font-semibold transition-all ${mode === 'form' ? 'bg-gradient-to-r from-violet-600 to-cyan-500 text-white' : 'liquid-btn'}`}
            style={mode !== 'form' ? { color: 'var(--text-primary)' } : {}}
          >
            <FileText className="w-4 h-4 inline mr-2" />
            Manual Entry
          </button>
          <button
            onClick={() => { setMode('upload'); setResult(null); }}
            className={`px-6 py-2 rounded-xl font-semibold transition-all ${mode === 'upload' ? 'bg-gradient-to-r from-violet-600 to-cyan-500 text-white' : 'liquid-btn'}`}
            style={mode !== 'upload' ? { color: 'var(--text-primary)' } : {}}
          >
            <Upload className="w-4 h-4 inline mr-2" />
            Upload Document
          </button>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {mode === 'form' ? (
            <div className="space-y-4">
              <div>
                <label style={{ color: 'var(--text-primary)' }} className="block mb-2 font-semibold">Submittal Name</label>
                <input
                  type="text"
                  value={submittal.submittal_name}
                  onChange={(e) => setSubmittal({ ...submittal, submittal_name: e.target.value })}
                  className="w-full liquid-btn px-4 py-3 rounded-xl outline-none"
                  style={{ color: 'var(--text-primary)' }}
                />
              </div>
              <div>
                <label style={{ color: 'var(--text-primary)' }} className="block mb-2 font-semibold">Battery Runtime (minutes)</label>
                <input
                  type="number"
                  value={submittal.battery_runtime_minutes}
                  onChange={(e) => setSubmittal({ ...submittal, battery_runtime_minutes: Number(e.target.value) })}
                  className="w-full liquid-btn px-4 py-3 rounded-xl outline-none"
                  style={{ color: 'var(--text-primary)' }}
                />
              </div>
              <div>
                <label style={{ color: 'var(--text-primary)' }} className="block mb-2 font-semibold">Redundancy</label>
                <select
                  value={submittal.redundancy}
                  onChange={(e) => setSubmittal({ ...submittal, redundancy: e.target.value })}
                  className="w-full liquid-btn px-4 py-3 rounded-xl outline-none"
                  style={{ color: 'var(--text-primary)' }}
                >
                  <option value="N">N</option>
                  <option value="N+1">N+1</option>
                  <option value="N+2">N+2</option>
                </select>
              </div>
              <div>
                <label style={{ color: 'var(--text-primary)' }} className="block mb-2 font-semibold">UPS Efficiency (%)</label>
                <input
                  type="number"
                  step="0.1"
                  value={submittal.ups_efficiency_percent}
                  onChange={(e) => setSubmittal({ ...submittal, ups_efficiency_percent: Number(e.target.value) })}
                  className="w-full liquid-btn px-4 py-3 rounded-xl outline-none"
                  style={{ color: 'var(--text-primary)' }}
                />
              </div>
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  id="chiller"
                  checked={submittal.chiller_n_plus_1}
                  onChange={(e) => setSubmittal({ ...submittal, chiller_n_plus_1: e.target.checked })}
                  className="w-5 h-5"
                />
                <label htmlFor="chiller" style={{ color: 'var(--text-primary)' }} className="font-semibold">Chiller N+1 Redundancy</label>
              </div>
              <button onClick={handleCheck} className="w-full bg-gradient-to-r from-violet-600 to-cyan-500 hover:from-violet-700 hover:to-cyan-600 text-white font-bold py-4 rounded-2xl shadow-2xl">
                Check Compliance
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <div
                className="border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer hover:border-violet-500 transition-all"
                style={{ borderColor: 'var(--glass-border)' }}
                onClick={() => fileInputRef.current?.click()}
              >
                <Upload className="w-12 h-12 mx-auto mb-4" style={{ color: 'var(--text-secondary)' }} />
                <p className="text-lg font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>
                  {file ? file.name : 'Click to upload a submittal document'}
                </p>
                <p style={{ color: 'var(--text-secondary)' }} className="text-sm">
                  PDF or TXT files supported
                </p>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.txt"
                  onChange={handleFileSelect}
                  className="hidden"
                />
              </div>
              {file && (
                <button
                  onClick={handleFileUpload}
                  disabled={uploading}
                  className="w-full bg-gradient-to-r from-violet-600 to-cyan-500 hover:from-violet-700 hover:to-cyan-600 text-white font-bold py-4 rounded-2xl shadow-2xl disabled:opacity-50"
                >
                  {uploading ? 'Analyzing with Antigravity Agent...' : 'Upload & Analyze'}
                </button>
              )}
            </div>
          )}

          {result && (
            <div className="space-y-4">
              <div className={`liquid-panel p-4 ${result.overall_compliant ? 'border-emerald-400' : 'border-coral-danger'} border-2`}>
                <div className="flex items-center gap-3 mb-2">
                  {result.overall_compliant ? <CheckCircle className="w-8 h-8 text-emerald-400" /> : <XCircle className="w-8 h-8 text-coral-danger" />}
                  <div>
                    <p className="text-xl font-bold" style={{ color: 'var(--text-primary)' }}>{result.submittal_name}</p>
                    <p className="text-3xl font-extrabold gradient-text">{result.compliance_score}% Compliant</p>
                    {result.summary && (
                      <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>{result.summary}</p>
                    )}
                  </div>
                </div>
              </div>
              {result.checks && result.checks.map((check, i) => (
                <div key={i} className="liquid-panel p-4 flex items-center justify-between">
                  <div>
                    <p className="font-bold" style={{ color: 'var(--text-primary)' }}>{check.parameter}</p>
                    <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>{check.standard} · Required: {check.required}</p>
                    <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>Submitted: {check.submitted}</p>
                  </div>
                  {check.compliant ? <CheckCircle className="w-6 h-6 text-emerald-400" /> : <XCircle className="w-6 h-6 text-coral-danger" />}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
