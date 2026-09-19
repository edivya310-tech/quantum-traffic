import React, { useState, useEffect } from 'react';
import { getComparisonSummary } from '../utils/api';
import { pctChange } from '../data/comparison';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Info } from 'lucide-react';

const ClassicalVsHybrid = () => {
  const [metrics, setMetrics] = useState([]);

  useEffect(() => {
    const fetchSummary = async () => {
      const data = await getComparisonSummary();
      setMetrics(data);
    };
    fetchSummary();
  }, []);

  return (
    <div className="max-w-6xl mx-auto space-y-6 flex flex-col h-full overflow-y-auto">
      <header>
        <div className="inline-block px-3 py-1 bg-warn/10 border border-warn/30 text-warn text-xs font-mono font-bold mb-4 rounded">
          DEMO / SIMULATED RESULTS
        </div>
        <h1 className="text-2xl md:text-3xl font-bold tracking-tight">Classical vs Hybrid Performance</h1>
        <p className="text-secondary mt-1">Aggregated benchmark results comparing standard SCATS/SCOOT logic vs QAOA optimization.</p>
      </header>

      {/* Candor paragraph */}
      <div className="bg-elevated border-l-4 border-cyan p-4 rounded text-sm text-secondary flex items-start space-x-3 shrink-0">
        <Info className="w-5 h-5 text-cyan shrink-0 mt-0.5" />
        <p>
          <strong className="text-primary">What's real vs simulated:</strong> The baseline values here are simulated benchmarks. In a production environment, this dashboard would ingest real historical SCATS data as the classical baseline, and run a calibrated SUMO micro-simulation powered by IBM Qiskit backend services to generate the hybrid results.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {metrics.map((m, i) => {
          const improvement = pctChange(m.classical, m.hybrid);
          // If inverse (lower is better), a negative change is good (text-go).
          // If not inverse (higher is better), a positive change is good (text-go).
          const isGood = m.inverse ? improvement < 0 : improvement > 0;
          
          return (
            <div key={i} className="bg-panel border border-border-subtle rounded-lg p-5">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-sm font-bold text-primary">{m.label}</h3>
                  <span className="text-xs text-muted font-mono">{m.unit}</span>
                </div>
                {/* Improvement Chip */}
                <div className={`px-2 py-1 rounded text-xs font-mono font-bold ${isGood ? 'bg-go/10 text-go border border-go/20' : 'bg-stop/10 text-stop border border-stop/20'}`}>
                  {improvement > 0 ? '+' : ''}{improvement}%
                </div>
              </div>

              <div className="h-40 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={[m]} layout="vertical" margin={{ top: 0, right: 30, left: 0, bottom: 0 }}>
                    <XAxis type="number" hide />
                    <YAxis dataKey="label" type="category" hide />
                    <Tooltip 
                      cursor={{fill: 'transparent'}}
                      contentStyle={{ backgroundColor: '#0f1420', borderColor: '#1c2436', color: '#eef2f8', fontFamily: 'monospace' }}
                      itemStyle={{ fontSize: '14px' }}
                    />
                    <Bar dataKey="classical" name="Classical" fill="#ef4444" radius={[0, 4, 4, 0]} barSize={24} />
                    <Bar dataKey="hybrid" name="Hybrid (QAOA)" fill="#22d3ee" radius={[0, 4, 4, 0]} barSize={24} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ClassicalVsHybrid;
