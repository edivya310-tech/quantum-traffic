import React, { useState } from 'react';
import { useTraffic } from '../context/TrafficContext';
import { runOptimization } from '../utils/api';
import ExplainabilityPanel from '../components/ExplainabilityPanel';
import { Zap, Play, CheckCircle2, ChevronRight, Activity } from 'lucide-react';

const QuantumOptimizer = () => {
  const { intersections, applyOptimizedPlan } = useTraffic();
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [plan, setPlan] = useState(null);
  const [selectedPlanItem, setSelectedPlanItem] = useState(null);

  const handleRunOptimization = async () => {
    setIsOptimizing(true);
    setPlan(null);
    setSelectedPlanItem(null);
    setProgress(0);
    
    // Simulate pipeline stages
    const stages = [20, 50, 80, 100];
    for (const p of stages) {
      await new Promise(r => setTimeout(r, 400));
      setProgress(p);
    }
    
    const newPlan = await runOptimization(intersections);
    setPlan(newPlan);
    setIsOptimizing(false);
  };

  const handleApply = () => {
    if (plan) {
      applyOptimizedPlan(plan);
      setPlan(null);
    }
  };

  const quboVariables = Array.from({ length: 16 }, (_, i) => `x${i + 1}`);

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <header>
        <div className="inline-block px-3 py-1 bg-cyan/10 border border-cyan/30 text-cyan text-xs font-mono font-bold mb-4 rounded">
          SIMULATION / FRONTEND DEMO — quantum backend integration pending
        </div>
        <h1 className="text-2xl md:text-3xl font-bold tracking-tight">Quantum Optimizer</h1>
        <p className="text-secondary mt-1">Hybrid classical-quantum signal timing optimization via QAOA.</p>
      </header>

      {/* Pipeline */}
      <div className="bg-panel border border-border-subtle rounded-lg p-6">
        <h2 className="text-[11px] uppercase tracking-widest text-muted font-semibold mb-6">Optimization Pipeline</h2>
        <div className="flex items-center justify-between font-mono text-sm">
          <div className={`flex flex-col items-center ${progress >= 0 ? 'text-primary' : 'text-muted'}`}>
            <div className={`w-10 h-10 rounded-full border-2 flex items-center justify-center mb-2 ${progress >= 0 ? 'border-cyan bg-cyan/10' : 'border-border-strong'}`}>1</div>
            <span className="text-center text-xs">State Capture</span>
          </div>
          <div className={`flex-1 h-px mx-4 ${progress >= 20 ? 'bg-cyan' : 'bg-border-strong'}`} />
          
          <div className={`flex flex-col items-center ${progress >= 20 ? 'text-primary' : 'text-muted'}`}>
            <div className={`w-10 h-10 rounded-full border-2 flex items-center justify-center mb-2 ${progress >= 20 ? 'border-cyan bg-cyan/10' : 'border-border-strong'}`}>2</div>
            <span className="text-center text-xs">QUBO Formulation</span>
          </div>
          <div className={`flex-1 h-px mx-4 ${progress >= 50 ? 'bg-cyan' : 'bg-border-strong'}`} />
          
          <div className={`flex flex-col items-center ${progress >= 50 ? 'text-primary' : 'text-muted'}`}>
            <div className={`w-10 h-10 rounded-full border-2 flex items-center justify-center mb-2 ${progress >= 50 ? 'border-cyan bg-cyan/10' : 'border-border-strong'}`}>3</div>
            <span className="text-center text-xs">QAOA Execution</span>
          </div>
          <div className={`flex-1 h-px mx-4 ${progress >= 80 ? 'bg-cyan' : 'bg-border-strong'}`} />
          
          <div className={`flex flex-col items-center ${progress >= 80 ? 'text-primary' : 'text-muted'}`}>
            <div className={`w-10 h-10 rounded-full border-2 flex items-center justify-center mb-2 ${progress >= 80 ? 'border-cyan bg-cyan/10' : 'border-border-strong'}`}>4</div>
            <span className="text-center text-xs">Hybrid Plan</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Input formulation */}
        <div className="space-y-6">
          <div className="bg-panel border border-border-subtle rounded-lg p-6">
            <h2 className="text-[11px] uppercase tracking-widest text-muted font-semibold mb-4">QUBO Variables</h2>
            
            <div className="flex gap-4">
              {/* QUBO List */}
              <div className="flex-1 font-mono text-xs text-secondary grid grid-cols-4 gap-2">
                {quboVariables.map(v => (
                  <div key={v} className="bg-base border border-border-strong px-2 py-1 rounded text-center">{v}</div>
                ))}
              </div>
              
              {/* Heatmap Upgrade */}
              <div className="w-32 h-32 shrink-0 grid grid-cols-4 gap-0.5 border border-border-strong p-1 rounded bg-base">
                {Array.from({length: 16}).map((_, i) => (
                  <div key={i} className="rounded-sm" style={{ backgroundColor: `rgba(34, 211, 238, ${Math.random() * 0.8 + 0.1})`}} />
                ))}
              </div>
            </div>
          </div>

          <button 
            onClick={handleRunOptimization}
            disabled={isOptimizing}
            className="w-full py-4 rounded-lg bg-cyan text-void font-bold tracking-wider hover:bg-cyan/90 transition-colors disabled:opacity-50 flex items-center justify-center space-x-2"
          >
            {isOptimizing ? (
              <>
                <Activity className="w-5 h-5 animate-pulse" />
                <span>OPTIMIZING... {progress}%</span>
              </>
            ) : (
              <>
                <Zap className="w-5 h-5" />
                <span>RUN QAOA OPTIMIZATION</span>
              </>
            )}
          </button>
        </div>

        {/* Right Column: Output Plan */}
        <div className="bg-panel border border-border-subtle rounded-lg p-6 flex flex-col h-[500px]">
          <h2 className="text-[11px] uppercase tracking-widest text-muted font-semibold mb-4">Proposed Plan</h2>
          
          {!plan && !isOptimizing && (
             <div className="flex-1 flex items-center justify-center text-muted font-mono border-2 border-dashed border-border-strong rounded-lg">
               AWAITING EXECUTION
             </div>
          )}

          {isOptimizing && (
            <div className="flex-1 flex flex-col items-center justify-center text-cyan font-mono border-2 border-dashed border-cyan/30 rounded-lg bg-cyan/5">
              <Activity className="w-8 h-8 mb-4 animate-bounce" />
              <div className="animate-pulse">SAMPLING QUANTUM STATES...</div>
            </div>
          )}

          {plan && (
            <div className="flex-1 flex flex-col min-h-0">
              <div className="flex-1 overflow-y-auto mb-4 border border-border-subtle rounded">
                <table className="w-full text-left font-mono text-sm">
                  <thead className="bg-base text-xs text-muted sticky top-0">
                    <tr>
                      <th className="p-3 border-b border-border-subtle">Node</th>
                      <th className="p-3 border-b border-border-subtle">Before</th>
                      <th className="p-3 border-b border-border-subtle">After</th>
                      <th className="p-3 border-b border-border-subtle">Delta</th>
                    </tr>
                  </thead>
                  <tbody>
                    {plan.map((item) => (
                      <tr 
                        key={item.id} 
                        onClick={() => setSelectedPlanItem(item)}
                        className={`border-b border-border-subtle cursor-pointer transition-colors ${selectedPlanItem?.id === item.id ? 'bg-cyan/10' : 'hover:bg-elevated'}`}
                      >
                        <td className="p-3 font-bold">{item.id}</td>
                        <td className="p-3 text-secondary">{item.before}s</td>
                        <td className="p-3 text-primary">{item.after}s</td>
                        <td className="p-3">
                          <span className={`px-2 py-1 rounded text-xs ${item.delta > 0 ? 'bg-go/20 text-go' : item.delta < 0 ? 'bg-warn/20 text-warn' : 'bg-base text-secondary'}`}>
                            {item.delta > 0 ? '+' : ''}{item.delta}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {selectedPlanItem && (
                <div className="mb-4 shrink-0">
                   <ExplainabilityPanel nodeId={selectedPlanItem.id} delta={selectedPlanItem.delta} />
                </div>
              )}

              <button 
                onClick={handleApply}
                className="w-full py-3 bg-go text-void font-bold rounded hover:bg-go/90 transition-colors flex items-center justify-center space-x-2 shrink-0"
              >
                <CheckCircle2 className="w-5 h-5" />
                <span>APPLY OPTIMIZED PLAN</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default QuantumOptimizer;
