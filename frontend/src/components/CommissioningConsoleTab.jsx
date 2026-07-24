import { useState } from 'react';
import { CheckCircle, XCircle, AlertTriangle, PlayCircle, RefreshCw } from 'lucide-react';

export default function CommissioningConsoleTab({ steps, onInjectDelay }) {
  const [selectedStep, setSelectedStep] = useState(steps[0] || null);
  const [testNotes, setTestNotes] = useState('');
  const [evaluation, setEvaluation] = useState(null);
  const [stepStatuses, setStepStatuses] = useState({});

  const handleEvaluate = async () => {
    const response = await fetch('/api/commissioning/evaluate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ test_notes: testNotes })
    });
    const data = await response.json();
    setEvaluation(data);
    setStepStatuses({ ...stepStatuses, [activeStep.id]: data.status });

    if (data.status === 'fail') {
      onInjectDelay(data.risk_task_ids, data.delay_days);
    }
  };

  const getStatusIcon = (status) => {
    if (status === 'pass') return <CheckCircle className="w-5 h-5 text-emerald-400" />;
    if (status === 'fail') return <XCircle className="w-5 h-5 text-coral-danger" />;
    if (status === 'warning') return <AlertTriangle className="w-5 h-5 text-amber-warning" />;
    return null;
  };

  if (!steps || steps.length === 0) {
    return <div className="liquid-panel p-6 text-center" style={{ color: 'var(--text-secondary)' }}>Loading commissioning steps...</div>;
  }

  const activeStep = selectedStep || steps[0];

  return (
    <div className="grid lg:grid-cols-3 gap-6">
      <div className="liquid-panel p-6">
        <h2 className="text-2xl font-bold mb-6" style={{ color: 'var(--text-primary)' }}>Commissioning Steps</h2>
        <div className="space-y-3">
          {steps.map(step => (
            <button
              key={step.id}
              onClick={() => { setSelectedStep(step); setEvaluation(null); setTestNotes(''); }}
              className={`w-full liquid-panel p-4 text-left transition-all ${activeStep && activeStep.id === step.id ? 'border-2 border-violet-500' : ''}`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-bold" style={{ color: 'var(--text-primary)' }}>{step.id}. {step.name}</p>
                  <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>{step.category}</p>
                </div>
                {getStatusIcon(stepStatuses[step.id])}
              </div>
            </button>
          ))}
        </div>
      </div>

      <div className="lg:col-span-2 space-y-6">
        <div className="liquid-panel p-6">
          <div className="flex items-center gap-3 mb-6">
            <PlayCircle className="w-7 h-7 text-violet-400" />
            <div>
              <h2 className="text-2xl font-bold" style={{ color: 'var(--text-primary)' }}>{activeStep.name}</h2>
              <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>{activeStep.category} · Step {activeStep.id} of {steps.length}</p>
            </div>
          </div>
          <p className="mb-6" style={{ color: 'var(--text-secondary)' }}>{activeStep.description}</p>

          <div className="mb-6">
            <label style={{ color: 'var(--text-primary)' }} className="block mb-2 font-semibold">Test Notes / Observations</label>
            <textarea
              value={testNotes}
              onChange={(e) => setTestNotes(e.target.value)}
              rows={5}
              placeholder="e.g., Generator ran for 4 hours at full load without issues."
              className="w-full liquid-btn px-4 py-3 rounded-xl outline-none resize-none"
              style={{ color: 'var(--text-primary)' }}
            />
          </div>

          <button onClick={handleEvaluate} className="w-full bg-gradient-to-r from-violet-600 to-cyan-500 hover:from-violet-700 hover:to-cyan-600 text-white font-bold py-4 rounded-2xl shadow-2xl flex items-center justify-center gap-2">
            <RefreshCw className="w-5 h-5" />
            Evaluate Test Result
          </button>

          {evaluation && (
            <div className={`mt-6 liquid-panel p-6 ${evaluation.status === 'fail' ? 'border-2 border-coral-danger' : evaluation.status === 'warning' ? 'border-2 border-amber-warning' : 'border-2 border-emerald-400'}`}>
              <div className="flex items-center gap-3 mb-4">
                {evaluation.status === 'pass' ? <CheckCircle className="w-10 h-10 text-emerald-400" /> : evaluation.status === 'fail' ? <XCircle className="w-10 h-10 text-coral-danger" /> : <AlertTriangle className="w-10 h-10 text-amber-warning" />}
                <div>
                  <p className="text-2xl font-bold capitalize" style={{ color: 'var(--text-primary)' }}>{evaluation.status}</p>
                  <p style={{ color: 'var(--text-secondary)' }}>{evaluation.summary}</p>
                </div>
              </div>
              {evaluation.delay_days > 0 && (
                <div className="liquid-panel p-4 mt-4 bg-coral-danger bg-opacity-10">
                  <p className="text-coral-danger font-bold">Auto-Injected Delay: +{evaluation.delay_days} days to critical path tasks</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
