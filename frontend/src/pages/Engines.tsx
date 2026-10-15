import { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function Engines() {
  const [engines, setEngines] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getEngines().then(data => {
      setEngines(data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Fleet Monitoring</h1>
      {loading ? (
        <div className="text-slate-500">Loading fleet data...</div>
      ) : (
        <div className="bg-white border border-slate-200 rounded-md shadow-sm overflow-hidden">
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Engine ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Max Cycles Logged</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Status</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-slate-200">
              {engines.map((e: any) => (
                <tr key={e.engine_id} className="hover:bg-slate-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">Engine {e.engine_id}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500 tabular-data">{e.cycle}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      Data Available
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
