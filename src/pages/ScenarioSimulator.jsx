import React, { useState } from 'react';
import { useTraffic } from '../context/TrafficContext';
import TrafficNetwork from '../components/TrafficNetwork';
import { runScenario } from '../utils/api';
import { Settings, Play, RefreshCcw, Activity } from 'lucide-react';
import { cn } from '../utils/format';

const PRESETS = [
  { label: 'Rush Hour Gridlock', intensity: 80, location: 'I4' },
  { label: 'I2 Accident', intensity: 95, location: 'I2' },
  { label: 'Moderate Weather', intensity: 40, location: 'I5' },
];

const NODES = ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8'];

const ScenarioSimulator = () => {
  const { applyScenarioImpact, applyScenarioOptimization, resetNetwork, scenarioState, intersections } = useTraffic();
  
  const [intensity, setIntensity] = useState(50);
  const [location, setLocation] = useState('I4');
  const [isSimulating, setIsSimulating] = useState(false);

  const handleApplyPreset = (preset) => {
    setIntensity(preset.intensity);
    setLocation(preset.location);
  };

  const handleRunScenario = async () => {
    setIsSimulating(true);
    const result = await runScenario({ intensity, location });
    applyScenarioImpact(result.impact, { intensity, location });
    setIsSimulating(false);
  };

  const handleOptimize = async () => {
    setIsSimulating(true);
    const result = await runScenario({ intensity, location }); // Reuse API to get optimized
    applyScenarioOptimization(result.optimized);
    setIsSimulating(false);
  };

  const handleReset = () => {
    resetNetwork();
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6 flex flex-col h-full">
      <header>
        <h1 className="text-2xl md:text-3xl font-bold tracking-tight">Scenario Simulator</h1>
        <p className="text-secondary mt-1">Stress-test the quantum optimization engine against anomalies.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1 min-h-0">
        
        {/* Left Column: Controls */}
        <div className="bg-panel border border-border-subtle rounded-lg p-6 flex flex-col overflow-y-auto">
          <h2 className="text-[11px] uppercase tracking-widest text-muted font-semibold mb-4 flex items-center"><Settings className="w-4 h-4 mr-2" /> Parameters</h2>
          
          <div className="mb-6 space-y-2">
             <label className="text-xs text-secondary mb-2 block">Quick Presets</label>
             <div className="flex flex-wrap gap-2">
               {PRESETS.map(p => (
                 <button 
                  key={p.label}
                  onClick={() => handleApplyPreset(p)}
                  className="px-3 py-1.5 bg-base border border-border-strong rounded-full text-xs font-mono text-primary hover:border-cyan transition-colors"
                 >
                   {p.label}
                 </button>
               ))}
             </div>
          </div>

          <div className="space-y-6 flex-1">
            <div>
              <div className="flex justify-between items-end mb-2">
                <label className="text-xs text-secondary block">Disruption Intensity</label>
                <span className="font-mono text-cyan text-sm">{intensity}%</span>
              </div>
              <input 
                type="range" 
                min="0" max="100" 
                value={intensity}
                onChange={(e) => setIntensity(Number(e.target.value))}
                className="w-full accent-cyan"
              />
            </div>
            
            <div>
              <label className="text-xs text-secondary mb-1 block">Epicenter Location</label>
              <select 
                value={location} 
                onChange={(e) => setLocation(e.target.value)}
                className="w-full bg-base border border-border-strong rounded p-2 text-primary font-mono focus:border-cyan outline-none"
              >
                {NODES.map(n => <option key={n} value={n}>{n}</option>)}
              </select>
            </div>
          </div>

          <div className="space-y-3 mt-6 pt-6 border-t border-border-subtle shrink-0">
            <button 
              onClick={handleRunScenario}
              disabled={isSimulating}
              className="w-full py-3 rounded bg-congestion text-white font-bold tracking-wider hover:bg-congestion/90 transition-colors disabled:opacity-50 flex items-center justify-center space-x-2"
            >
              <Play className="w-4 h-4" />
              <span>APPLY IMPACT</span>
            </button>
            
            <button 
              onClick={handleOptimize}
              disabled={isSimulating || scenarioState?.status !== 'impacted'}
              className="w-full py-3 rounded bg-cyan text-void font-bold tracking-wider hover:bg-cyan/90 transition-colors disabled:opacity-50 flex items-center justify-center space-x-2"
            >
              <Activity className="w-4 h-4" />
              <span>OPTIMIZE RESPONSE</span>
            </button>

            <button 
              onClick={handleReset}
              className="w-full py-3 rounded bg-transparent border border-border-strong text-secondary font-bold tracking-wider hover:bg-base hover:text-primary transition-colors flex items-center justify-center space-x-2"
            >
              <RefreshCcw className="w-4 h-4" />
              <span>RESET TO BASELINE</span>
            </button>
          </div>
        </div>

        {/* Right Column: Mini Networks Comparison */}
        <div className="lg:col-span-2 bg-panel border border-border-subtle rounded-lg p-6 flex flex-col min-h-0">
           <div className="flex items-center justify-between mb-4 shrink-0">
             <h2 className="text-[11px] uppercase tracking-widest text-muted font-semibold">Network State Comparison</h2>
             <div className="font-mono text-xs">
               Status: <span className={cn("font-bold", !scenarioState ? 'text-primary' : scenarioState.status === 'impacted' ? 'text-congestion' : 'text-cyan')}>{!scenarioState ? 'BASELINE' : scenarioState.status.toUpperCase()}</span>
             </div>
           </div>

           <div className="flex-1 flex flex-col md:flex-row gap-6 min-h-0 items-center justify-center">
              {/* Baseline / Current */}
              <div className="flex-1 w-full flex flex-col items-center">
                <span className="text-xs font-mono text-secondary mb-2">Live View</span>
                <div className="w-full max-w-[300px]">
                  <TrafficNetwork compact={true} />
                </div>
              </div>

              {/* Just a divider */}
              <div className="hidden md:block w-px bg-border-subtle h-1/2"></div>
              
              {/* Impact readout stats */}
              <div className="flex-1 w-full flex flex-col justify-center space-y-4 px-4 font-mono text-sm">
                 <div className="bg-base border border-border-subtle p-3 rounded flex justify-between">
                   <span className="text-muted">Total Queue</span>
                   <span className="text-primary">{intersections.reduce((s, i) => s + i.queue, 0)}</span>
                 </div>
                 <div className="bg-base border border-border-subtle p-3 rounded flex justify-between">
                   <span className="text-muted">Avg Wait</span>
                   <span className="text-primary">{Math.round(intersections.reduce((s, i) => s + i.waiting, 0)/8)}s</span>
                 </div>
                 <div className="bg-base border border-border-subtle p-3 rounded flex justify-between">
                   <span className="text-muted">Throughput</span>
                   <span className="text-primary">{intersections.reduce((s, i) => s + i.throughput, 0)}/m</span>
                 </div>
              </div>
           </div>
        </div>
      </div>
    </div>
  );
};

export default ScenarioSimulator;
