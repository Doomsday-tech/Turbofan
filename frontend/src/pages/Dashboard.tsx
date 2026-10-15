import { useEffect, useState } from 'react';
import { Activity, AlertCircle, CheckCircle2 } from 'lucide-react';
import { api } from '../services/api';

export default function Dashboard() {
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getSummary()
      .then(data => {
        setSummary(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="flex justify-center mt-20 text-slate-500">Loading system data...</div>;
  }

  if (!summary || summary.error) {
    return (
      <div className="bg-white border border-slate-200 rounded-md p-10 text-center max-w-2xl mx-auto mt-10">
        <AlertCircle className="w-12 h-12 text-slate-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-slate-900">Model Not Loaded</h2>
        <p className="text-slate-600 mt-2">The machine learning model has not been trained or the backend is offline.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between pb-4 border-b border-slate-200">
        <h1 className="text-2xl font-bold text-slate-900">System Overview</h1>
        <div className="flex items-center gap-2 bg-green-50 text-green-700 px-3 py-1.5 rounded-full text-sm font-medium border border-green-200">
          <CheckCircle2 className="w-4 h-4" />
          API Connected
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-md border border-slate-200 shadow-sm">
          <p className="text-sm font-medium text-slate-500 mb-1">Active Model</p>
          <p className="text-lg font-semibold text-slate-900">{summary.metadata.model_name}</p>
        </div>
        <div className="bg-white p-6 rounded-md border border-slate-200 shadow-sm">
          <p className="text-sm font-medium text-slate-500 mb-1">Engines Monitored</p>
          <p className="text-3xl font-bold text-slate-900 tabular-data">{summary.metadata.engines_evaluated}</p>
        </div>
        <div className="bg-white p-6 rounded-md border border-slate-200 shadow-sm">
          <p className="text-sm font-medium text-slate-500 mb-1">Alert Threshold</p>
          <p className="text-3xl font-bold text-slate-900 tabular-data">≤ {summary.threshold} <span className="text-sm font-normal text-slate-500">cycles</span></p>
        </div>
      </div>

      <h2 className="text-lg font-semibold text-slate-900 mt-8 mb-4">Model Performance (Official Evaluation)</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-md border border-slate-200 shadow-sm">
          <p className="text-sm font-medium text-slate-500 mb-1">RMSE</p>
          <p className="text-2xl font-bold text-slate-900 tabular-data">{summary.metrics.rmse.toFixed(2)}</p>
        </div>
        <div className="bg-white p-6 rounded-md border border-slate-200 shadow-sm">
          <p className="text-sm font-medium text-slate-500 mb-1">MAE</p>
          <p className="text-2xl font-bold text-slate-900 tabular-data">{summary.metrics.mae.toFixed(2)}</p>
        </div>
        <div className="bg-white p-6 rounded-md border border-slate-200 shadow-sm">
          <p className="text-sm font-medium text-slate-500 mb-1">NASA Asymmetric Score</p>
          <p className="text-2xl font-bold text-slate-900 tabular-data">{summary.metrics.nasa_score.toFixed(2)}</p>
        </div>
      </div>
    </div>
  );
}
