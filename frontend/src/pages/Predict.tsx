import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Play } from 'lucide-react';

export default function Predict() {
  const [engines, setEngines] = useState([]);
  const [selectedEngine, setSelectedEngine] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.getEngines().then(setEngines).catch(console.error);
  }, []);

  const runPrediction = async () => {
    if (!selectedEngine) return;
    setLoading(true);
    setResult(null);
    try {
      const history = await api.getEngineHistory(parseInt(selectedEngine));
      const prediction = await api.predict(history);
      setResult(prediction);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="space-y-6 max-w-3xl">
      <h1 className="text-2xl font-bold text-slate-900">Run Prediction</h1>
      
      <div className="bg-white p-6 border border-slate-200 rounded-md shadow-sm space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Select Engine from Dataset</label>
          <select 
            className="w-full border border-slate-300 rounded-md p-2 bg-slate-50"
            value={selectedEngine}
            onChange={(e) => setSelectedEngine(e.target.value)}
          >
            <option value="">-- Choose an Engine --</option>
            {engines.map((e: any) => (
              <option key={e.engine_id} value={e.engine_id}>Engine {e.engine_id} (Max Cycle: {e.cycle})</option>
            ))}
          </select>
        </div>
        <button 
          onClick={runPrediction}
          disabled={!selectedEngine || loading}
          className="flex items-center gap-2 bg-slate-900 text-white px-4 py-2 rounded-md hover:bg-slate-800 disabled:opacity-50 transition-colors"
        >
          <Play className="w-4 h-4" />
          {loading ? 'Running Inference...' : 'Run Model Prediction'}
        </button>
      </div>

      {result && !result.error && (
        <div className={`p-6 border rounded-md shadow-sm ${
          result.risk_category === 'danger' ? 'bg-red-50 border-red-200' : 
          result.risk_category === 'warning' ? 'bg-amber-50 border-amber-200' : 
          'bg-green-50 border-green-200'
        }`}>
          <h2 className="text-lg font-bold mb-4 text-slate-900">Prediction Results</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-sm font-medium text-slate-600">Remaining Useful Life (RUL)</p>
              <p className="text-4xl font-bold tabular-data text-slate-900 mt-1">{result.predicted_rul} <span className="text-sm font-normal text-slate-600">cycles</span></p>
            </div>
            <div>
              <p className="text-sm font-medium text-slate-600">Alert Status</p>
              <p className={`text-xl font-bold mt-1 ${
                result.risk_category === 'danger' ? 'text-red-700' : 
                result.risk_category === 'warning' ? 'text-amber-700' : 
                'text-green-700'
              }`}>{result.alert_status}</p>
              <p className="text-sm text-slate-500 mt-1">Threshold: {result.threshold} cycles</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
