import { Outlet, NavLink } from 'react-router-dom';
import { Activity, Server, LayoutDashboard, Settings, AlertTriangle } from 'lucide-react';

export default function MainLayout() {
  const navItems = [
    { path: '/', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/engines', label: 'Fleet Monitoring', icon: Activity },
    { path: '/predict', label: 'Run Prediction', icon: Server },
    { path: '/alerts', label: 'Active Alerts', icon: AlertTriangle },
    { path: '/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div className="flex h-screen w-full bg-slate-50 overflow-hidden">
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col">
        <div className="p-4 border-b border-slate-200">
          <h1 className="font-bold text-slate-900 flex items-center gap-2">
            <Activity className="w-5 h-5 text-slate-700" />
            Turbofan RUL
          </h1>
          <p className="text-xs text-slate-600 mt-1">Predictive Maintenance</p>
        </div>
        
        <nav className="flex-1 p-4 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive 
                    ? 'bg-slate-900 text-white' 
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                }`
              }
            >
              <item.icon className="w-4 h-4" />
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>

      <main className="flex-1 flex flex-col h-full overflow-auto">
        <div className="p-8 max-w-7xl mx-auto w-full">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
