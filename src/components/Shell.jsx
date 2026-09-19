import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { Activity, Network, Zap, ShieldAlert, Cpu, Leaf, BarChart2, GitFork } from 'lucide-react';
import { useTraffic } from '../context/TrafficContext';

const NAV_ITEMS = [
  { path: '/command-center', label: 'COMMAND CENTER', icon: Activity },
  { path: '/optimizer', label: 'QUANTUM OPTIMIZER', icon: Zap },
  { path: '/emergency', label: 'EMERGENCY CORRIDOR', icon: ShieldAlert },
  { path: '/scenario', label: 'SCENARIO SIMULATOR', icon: Cpu },
  { path: '/environment', label: 'ENVIRONMENT', icon: Leaf },
  { path: '/comparison', label: 'CLASSICAL vs HYBRID', icon: BarChart2 },
  { path: '/architecture', label: 'ARCHITECTURE', icon: GitFork },
];

const Shell = ({ children }) => {
  const { isLoading, emergency } = useTraffic();

  return (
    <div className="flex h-screen bg-void text-primary font-sans overflow-hidden">
      {/* Sidebar */}
      <aside className="w-[256px] flex-shrink-0 bg-base border-r border-border-subtle flex flex-col hidden lg:flex">
        <div className="p-6">
          <div className="flex items-center space-x-3 mb-2">
            <Network className="w-6 h-6 text-cyan" />
            <h1 className="font-bold tracking-wider text-sm">Q-TRAFFIC</h1>
          </div>
          <p className="text-[10px] text-muted font-mono tracking-widest uppercase">
            Quantum Traffic OS
          </p>
        </div>
        
        <div className="px-4 mb-2">
          <div className="h-px bg-border-subtle w-full"></div>
        </div>

        <nav className="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => `
                flex items-center space-x-3 px-3 py-2.5 rounded text-xs font-semibold tracking-wider uppercase transition-colors duration-150
                ${isActive 
                  ? 'bg-cyan/10 text-cyan border-l-2 border-cyan' 
                  : 'text-secondary hover:text-primary hover:bg-elevated border-l-2 border-transparent'
                }
              `}
            >
              <item.icon className="w-4 h-4" />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="px-4 mt-auto mb-2">
          <div className="h-px bg-border-subtle w-full"></div>
        </div>

        <div className="p-6 pt-4">
          <h3 className="text-[10px] text-muted font-mono tracking-widest uppercase mb-3">
            System Status
          </h3>
          <div className="flex items-center space-x-2 font-mono text-xs">
            <div className={`w-2 h-2 rounded-full ${isLoading ? 'bg-warn animate-pulse' : (emergency.active ? 'bg-warn animate-pulse' : 'bg-go')}`}></div>
            <span className={isLoading ? 'text-warn' : (emergency.active ? 'text-warn' : 'text-go')}>
              {isLoading ? 'CONNECTING...' : (emergency.active ? 'EMERGENCY OVERRIDE' : 'ONLINE')}
            </span>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden bg-void relative">
        <div className="flex-1 overflow-y-auto p-4 lg:p-8">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Shell;
