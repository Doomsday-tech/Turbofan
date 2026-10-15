import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Save, Info } from 'lucide-react';

export default function Settings() {
  const [threshold, setThreshold] = useState(30);
  const [message, setMessage] = useState('');

  useEffect(() => {
    api.getSummary().then(data => {
      if (data && data.threshold) setThreshold(data.threshold);
    }).catch(console.error);
  }, []);

  const handleSave = async () => {
    try {
      const res = await fetch('http://127.0.0.1:5000/api/settings/threshold', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ threshold: Number(threshold) })
      });
      if (res.ok) setMessage('Threshold updated successfully in backend!');
      setTimeout(() => setMessage(''), 3000);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <h1 className="text-2xl font-bold text-slate-900">System Settings</h1>
      
      <div className="bg-white p-6 border border-slate-200 rounded-md shadow-sm space-y-6">
        <div className="flex gap-3 p-4 bg-blue-50 border border-blue-200 rounded-md text-blue-800 text-sm">
          <Info className="w-5 h-5 shrink-0" />
          <p>This threshold determines when an engine prediction triggers a <b>Warning</b> status. Predictions at or below 10 cycles are always marked as <b>Critical</b>.</p>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-slate-900 mb-1">RUL Warning Threshold (Cycles)</label>
          <input 
            type="number" 
            value={threshold}
            onChange={(e) => setThreshold(Number(e.target.value))}
            className="w-32 border border-slate-300 rounded-md p-2 tabular-data bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-slate-900"
          />
        </div>
        
        <button 
          onClick={handleSave}
          className="flex items-center gap-2 bg-slate-900 text-white px-4 py-2 rounded-md hover:bg-slate-800 transition-colors"
        >
          <Save className="w-4 h-4" />
          Save Settings
        </button>
        
        {message && <p className="text-green-600 text-sm font-medium">{message}</p>}
      </div>
    </div>
  );
}
