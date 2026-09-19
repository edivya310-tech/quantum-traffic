import React, { useState, useEffect } from 'react';
import { getEnvironmentTimeseries } from '../utils/api';
import { useTraffic } from '../context/TrafficContext';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Leaf, Info } from 'lucide-react';

const Environment = () => {
  const [data, setData] = useState([]);
  const { lastOptimization } = useTraffic();
  const [savings, setSavings] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      const ts = await getEnvironmentTimeseries();
      setData(ts);
    };
    fetchData();
  }, []);

  // Mock savings counter based on optimizations applied
  useEffect(() => {
    if (lastOptimization) {
      setSavings(prev => prev + Math.floor(Math.random() * 50) + 10);
    }
  }, [lastOptimization]);

  return (
    <div className="max-w-6xl mx-auto space-y-6 flex flex-col h-full">
      <header className="flex justify-between items-end">
        <div>
          <div className="inline-block px-3 py-1 bg-cyan/10 border border-cyan/30 text-cyan text-xs font-mono font-bold mb-4 rounded">
            SIMULATED ESTIMATES
          </div>
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight">Environmental Impact</h1>
          <p className="text-secondary mt-1">Real-time emissions tracking based on network flow efficiency.</p>
        </div>
        
        {/* Cumulative Savings Counter */}
        <div className="bg-panel border border-go/30 p-4 rounded-lg flex items-center space-x-4">
          <div className="p-3 bg-go/10 rounded-full text-go">
            <Leaf className="w-6 h-6" />
          </div>
          <div>
            <div className="text-[11px] uppercase tracking-widest text-muted font-semibold">Cumulative Savings</div>
            <div className="flex items-baseline space-x-1">
              <span className="text-3xl font-mono font-bold text-go">{savings}</span>
              <span className="text-sm font-mono text-secondary">kg CO2 avoided</span>
            </div>
          </div>
        </div>
      </header>

      {/* Methodology Note */}
      <div className="bg-elevated border-l-4 border-cyan p-4 rounded text-sm text-secondary flex items-start space-x-3 shrink-0">
        <Info className="w-5 h-5 text-cyan shrink-0 mt-0.5" />
        <p>
          <strong className="text-primary">Methodology Note:</strong> The figures displayed here are estimated from proxy variables (queue lengths, idle times, and stop-and-go occurrences). They are not measured emissions. A real deployment would integrate with IoT environmental sensors or EPA MOVES emission modeling.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 flex-1 min-h-0">
        {/* CO2 Chart */}
        <div className="bg-panel border border-border-subtle rounded-lg p-6 flex flex-col">
          <h2 className="text-[11px] uppercase tracking-widest text-muted font-semibold mb-4 shrink-0">CO2 Emissions Rate (kg/h)</h2>
          <div className="flex-1 min-h-0">
            {data.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorBaseline" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorHybrid" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#22c55e" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1c2436" vertical={false} />
                  <XAxis dataKey="time" stroke="#5c6a84" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#5c6a84" fontSize={12} tickLine={false} axisLine={false} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#0f1420', borderColor: '#1c2436', color: '#eef2f8', fontFamily: 'monospace' }}
                    itemStyle={{ fontSize: '14px' }}
                  />
                  <Area type="monotone" dataKey="baselineCO2" name="Classical" stroke="#ef4444" fillOpacity={1} fill="url(#colorBaseline)" strokeWidth={2} />
                  <Area type="monotone" dataKey="hybridCO2" name="Quantum-Hybrid" stroke="#22c55e" fillOpacity={1} fill="url(#colorHybrid)" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex h-full items-center justify-center font-mono text-muted">LOADING DATA...</div>
            )}
          </div>
        </div>

        {/* Fuel Chart */}
        <div className="bg-panel border border-border-subtle rounded-lg p-6 flex flex-col">
          <h2 className="text-[11px] uppercase tracking-widest text-muted font-semibold mb-4 shrink-0">Fuel Consumption (gal/h)</h2>
          <div className="flex-1 min-h-0">
            {data.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1c2436" vertical={false} />
                  <XAxis dataKey="time" stroke="#5c6a84" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#5c6a84" fontSize={12} tickLine={false} axisLine={false} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#0f1420', borderColor: '#1c2436', color: '#eef2f8', fontFamily: 'monospace' }}
                    itemStyle={{ fontSize: '14px' }}
                  />
                  <Area type="monotone" dataKey="baselineFuel" name="Classical" stroke="#ef4444" fillOpacity={1} fill="url(#colorBaseline)" strokeWidth={2} />
                  <Area type="monotone" dataKey="hybridFuel" name="Quantum-Hybrid" stroke="#22c55e" fillOpacity={1} fill="url(#colorHybrid)" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex h-full items-center justify-center font-mono text-muted">LOADING DATA...</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Environment;
