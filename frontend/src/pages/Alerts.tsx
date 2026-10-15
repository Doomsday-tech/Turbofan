import { AlertTriangle } from 'lucide-react';

export default function Alerts() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Active Alerts</h1>
      <div className="bg-white p-10 border border-slate-200 rounded-md shadow-sm text-center">
        <AlertTriangle className="w-12 h-12 text-slate-300 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-slate-900">No Active Fleet Alerts</h2>
        <p className="text-slate-500 mt-2 max-w-lg mx-auto">
          Alerts are generated when an engine's predicted RUL falls below the threshold configured in Settings. Go to the <b>Run Prediction</b> tab to evaluate an engine.
        </p>
      </div>
    </div>
  );
}
