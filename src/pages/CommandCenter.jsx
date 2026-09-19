import React, { useState } from 'react';
import { useTraffic } from '../context/TrafficContext';
import TrafficNetwork from '../components/TrafficNetwork';
import MetricCard from '../components/MetricCard';
import { Clock, Activity, Car, Cloud, Battery, ShieldAlert, X } from 'lucide-react';
import { calculateHealthScore, generatePredictiveCongestion } from '../utils/metrics';

const CommandCenter = () => {
  const { intersections, kpis, isLoading } = useTraffic();
  const [selectedNodeId, setSelectedNodeId] = useState(null);

  if (isLoading || !kpis) {
    return <div className="flex items-center justify-center h-full text-cyan font-mono animate-pulse">INITIALIZING SYSTEM...</div>;
  }

  const selectedNode = intersections.find(n => n.id === selectedNodeId);
  const healthScore = calculateHealthScore(kpis);
  const predictiveCongestion = generatePredictiveCongestion(intersections);

  return (
    <div className="flex flex-col h-full space-y-6">
      {/* Header */}
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight">Command Center</h1>
          <p className="text-secondary mt-1">Real-time network state and predictive insights</p>
        </div>
        
        {/* Network Health Score */}
        <div className="flex items-center space-x-4 bg-panel px-4 py-2 rounded border border-border-subtle">
          <div className="flex flex-col">
            <span className="text-[11px] uppercase tracking-widest text-muted">Network Health</span>
            <div className="flex items-baseline space-x-1">
              <span className={`text-2xl font-mono font-bold ${healthScore > 80 ? 'text-go' : healthScore > 50 ? 'text-warn' : 'text-stop'}`}>
                {healthScore}
              </span>
              <span className="text-xs text-muted">/100</span>
            </div>
          </div>
          {/* Radial gauge mock */}
          <div className="relative w-10 h-10 rounded-full border-4 border-border-strong flex items-center justify-center">
            <div 
              className="absolute inset-0 rounded-full border-4 border-cyan" 
              style={{ clipPath: `polygon(0 0, 100% 0, 100% ${healthScore}%, 0 ${healthScore}%)`, transform: 'rotate(-90deg)' }} 
            />
          </div>
        </div>
      </header>

      {/* Predictive Congestion Ribbon */}
      <div className="w-full h-12 bg-panel border border-border-subtle rounded flex items-center px-4 overflow-hidden relative">
        <div className="text-[10px] uppercase font-mono tracking-widest text-muted whitespace-nowrap mr-6 shrink-0 z-10 bg-panel py-1 pr-2">
          Predictive Forecast (15m)
        </div>
        <div className="flex-1 flex items-end h-full pt-4 pb-2 space-x-1 overflow-hidden opacity-80">
          {predictiveCongestion.map((pt, i) => (
            <div 
              key={i} 
              className="flex-1 bg-cyan/20 rounded-t border-t border-cyan/40 transition-all"
              style={{ height: `${pt.value * 100}%` }}
              title={`${pt.time}: ${Math.round(pt.value * 100)}%`}
            />
          ))}
        </div>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4">
        <MetricCard label="Avg Wait" value={kpis.waiting} unit="s" icon={Clock} />
        <MetricCard label="Throughput" value={kpis.throughput} unit="v/m" icon={Activity} />
        <MetricCard label="Queue Length" value={kpis.queue} unit="veh" icon={Car} />
        <MetricCard label="Est. CO2" value={kpis.co2} unit="kg/h" icon={Cloud} />
        <MetricCard label="Fuel Burn" value={kpis.fuel} unit="gal/h" icon={Battery} />
        <MetricCard label="Emergency ETA" value={kpis.emergencyETA} unit="min" icon={ShieldAlert} highlight={kpis.emergencyETA < 15} />
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col lg:flex-row gap-6 min-h-0">
        {/* Network Map */}
        <div className="flex-1 min-h-0 h-full flex flex-col">
          <div className="flex items-center space-x-2 mb-3">
            <div className="w-2 h-2 rounded-full bg-go animate-pulse" />
            <h2 className="text-[11px] uppercase tracking-widest text-secondary font-semibold">Live Network Map</h2>
          </div>
          <div className="flex-1">
             <TrafficNetwork selectedNodeId={selectedNodeId} onNodeClick={setSelectedNodeId} />
          </div>
        </div>

        {/* Docked Detail Panel */}
        {selectedNodeId && (
          <div className="w-full lg:w-[320px] bg-panel border border-border-subtle rounded-lg flex flex-col shrink-0">
            <div className="p-4 border-b border-border-subtle flex justify-between items-center bg-elevated rounded-t-lg">
              <h3 className="font-mono font-bold text-lg">Intersection {selectedNodeId}</h3>
              <button onClick={() => setSelectedNodeId(null)} className="text-muted hover:text-primary transition-colors">
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="p-4 space-y-4 overflow-y-auto">
              <div className="flex justify-between items-center bg-base p-3 rounded border border-border-subtle">
                <span className="text-xs text-muted uppercase">Signal State</span>
                <div className="flex items-center space-x-2 font-mono text-sm font-bold">
                  <div className={`w-3 h-3 rounded-full ${selectedNode.signal === 'GREEN' ? 'bg-go' : selectedNode.signal === 'YELLOW' ? 'bg-warn' : 'bg-stop'}`} />
                  <span className={selectedNode.signal === 'GREEN' ? 'text-go' : selectedNode.signal === 'YELLOW' ? 'text-warn' : 'text-stop'}>
                    {selectedNode.signal}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="bg-base p-3 rounded border border-border-subtle">
                  <div className="text-[10px] text-muted uppercase mb-1">Queue</div>
                  <div className="font-mono text-lg font-bold">{selectedNode.queue} <span className="text-xs text-muted">veh</span></div>
                </div>
                <div className="bg-base p-3 rounded border border-border-subtle">
                  <div className="text-[10px] text-muted uppercase mb-1">Wait Time</div>
                  <div className="font-mono text-lg font-bold">{selectedNode.waiting} <span className="text-xs text-muted">s</span></div>
                </div>
                <div className="bg-base p-3 rounded border border-border-subtle">
                  <div className="text-[10px] text-muted uppercase mb-1">Density</div>
                  <div className="font-mono text-lg font-bold">{Math.round(selectedNode.density * 100)}%</div>
                </div>
                <div className="bg-base p-3 rounded border border-border-subtle">
                  <div className="text-[10px] text-muted uppercase mb-1">Throughput</div>
                  <div className="font-mono text-lg font-bold">{selectedNode.throughput} <span className="text-xs text-muted">v/m</span></div>
                </div>
              </div>
              
              <div className="pt-4 border-t border-border-subtle">
                <h4 className="text-[10px] text-muted uppercase tracking-wider mb-3">Signal Timing Plan</h4>
                <div className="space-y-2 font-mono text-sm">
                  <div className="flex justify-between items-center">
                    <span className="text-go">GREEN</span>
                    <span>{selectedNode.greenDuration}s</span>
                  </div>
                  <div className="w-full bg-base h-2 rounded overflow-hidden">
                    <div className="bg-go h-full" style={{ width: `${(selectedNode.greenDuration / (selectedNode.greenDuration + selectedNode.redDuration)) * 100}%` }} />
                  </div>
                  <div className="flex justify-between items-center mt-2">
                    <span className="text-stop">RED</span>
                    <span>{selectedNode.redDuration}s</span>
                  </div>
                  <div className="w-full bg-base h-2 rounded overflow-hidden">
                    <div className="bg-stop h-full" style={{ width: `${(selectedNode.redDuration / (selectedNode.greenDuration + selectedNode.redDuration)) * 100}%` }} />
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CommandCenter;
