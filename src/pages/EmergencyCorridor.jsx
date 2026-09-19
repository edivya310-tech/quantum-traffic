import React, { useState, useEffect } from 'react';
import { useTraffic } from '../context/TrafficContext';
import TrafficNetwork from '../components/TrafficNetwork';
import { activateEmergency as activateEmergencyApi } from '../utils/api';
import { ShieldAlert, MapPin, Navigation, Clock, Activity, PowerOff } from 'lucide-react';

const NODES = ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8'];

const EmergencyCorridor = () => {
  const { emergency, activateEmergencyRoute, deactivateEmergency, intersections } = useTraffic();
  const [origin, setOrigin] = useState('I1');
  const [destination, setDestination] = useState('I8');
  const [isActivating, setIsActivating] = useState(false);
  const [eta, setEta] = useState(null);

  // Countdown timer effect
  useEffect(() => {
    let interval;
    if (emergency.active && eta > 0) {
      interval = setInterval(() => {
        setEta(prev => Math.max(0, prev - 1));
      }, 60000); // 1 minute per tick (simulated)
      // for demo, maybe tick faster? let's do 1 second = 1 min
    }
    return () => clearInterval(interval);
  }, [emergency.active, eta]);

  // faster demo tick
  useEffect(() => {
     let interval;
     if (emergency.active && eta > 0) {
       interval = setInterval(() => {
         setEta(prev => Math.max(0, prev - 1));
       }, 2000); 
     }
     return () => clearInterval(interval);
  }, [emergency.active, eta]);

  const handleActivate = async () => {
    if (origin === destination) return;
    setIsActivating(true);
    const data = await activateEmergencyApi({ origin, destination });
    activateEmergencyRoute({ ...data, origin, destination });
    setEta(12); // Mock ETA start
    setIsActivating(false);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6 flex flex-col h-full">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-warn">Emergency Corridor</h1>
          <p className="text-secondary mt-1">Pre-emptive green wave routing for emergency vehicles.</p>
        </div>
        {emergency.active && (
          <div className="flex items-center space-x-2 bg-warn/10 text-warn px-4 py-2 rounded border border-warn">
            <div className="w-3 h-3 rounded-full bg-warn animate-pulse" />
            <span className="font-mono font-bold tracking-widest uppercase">Corridor Active</span>
          </div>
        )}
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1 min-h-0">
        {/* Left Column: Controls & Timeline */}
        <div className="flex flex-col space-y-6 lg:col-span-1 overflow-y-auto">
          {/* Controls */}
          <div className="bg-panel border border-border-subtle rounded-lg p-6">
            <h2 className="text-[11px] uppercase tracking-widest text-muted font-semibold mb-4">Routing Parameters</h2>
            
            <div className="space-y-4">
              <div>
                <label className="text-xs text-secondary mb-1 block">Origin</label>
                <select 
                  disabled={emergency.active}
                  value={origin} 
                  onChange={(e) => setOrigin(e.target.value)}
                  className="w-full bg-base border border-border-strong rounded p-2 text-primary font-mono focus:border-cyan outline-none disabled:opacity-50"
                >
                  {NODES.map(n => <option key={n} value={n}>{n}</option>)}
                </select>
              </div>
              
              <div>
                <label className="text-xs text-secondary mb-1 block">Destination</label>
                <select 
                  disabled={emergency.active}
                  value={destination} 
                  onChange={(e) => setDestination(e.target.value)}
                  className="w-full bg-base border border-border-strong rounded p-2 text-primary font-mono focus:border-cyan outline-none disabled:opacity-50"
                >
                  {NODES.map(n => <option key={n} value={n}>{n}</option>)}
                </select>
              </div>

              {!emergency.active ? (
                <button 
                  onClick={handleActivate}
                  disabled={isActivating || origin === destination}
                  className="w-full py-3 mt-4 rounded bg-warn text-void font-bold tracking-wider hover:bg-warn/90 transition-colors disabled:opacity-50 flex items-center justify-center space-x-2"
                >
                  {isActivating ? <Activity className="w-5 h-5 animate-pulse" /> : <ShieldAlert className="w-5 h-5" />}
                  <span>ACTIVATE CORRIDOR</span>
                </button>
              ) : (
                <button 
                  onClick={deactivateEmergency}
                  className="w-full py-3 mt-4 rounded bg-border-strong text-primary font-bold tracking-wider hover:bg-border-subtle transition-colors flex items-center justify-center space-x-2"
                >
                  <PowerOff className="w-5 h-5" />
                  <span>DEACTIVATE & RESTORE</span>
                </button>
              )}
            </div>
          </div>

          {/* Timeline */}
          {emergency.active && (
            <div className="bg-panel border border-warn/30 rounded-lg p-6 flex-1">
               <h2 className="text-[11px] uppercase tracking-widest text-muted font-semibold mb-4">Event Log</h2>
               <div className="space-y-4 relative before:absolute before:inset-0 before:ml-2 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-border-subtle before:to-transparent">
                  {emergency.log.map((entry, idx) => (
                    <div key={idx} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                      <div className="flex items-center justify-center w-5 h-5 rounded-full border-2 border-warn bg-void text-warn shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow"></div>
                      <div className="w-[calc(100%-2rem)] md:w-[calc(50%-1.5rem)] bg-base p-3 rounded border border-border-subtle font-mono text-xs text-secondary">
                        {entry.message}
                      </div>
                    </div>
                  ))}
               </div>
            </div>
          )}
        </div>

        {/* Right Column: Map & Readouts */}
        <div className="lg:col-span-2 flex flex-col space-y-6 h-full min-h-0">
          
          {/* Readouts */}
          <div className="grid grid-cols-2 gap-4 shrink-0">
            <div className="bg-panel border border-border-subtle rounded-lg p-4 flex flex-col items-center justify-center">
              <span className="text-[11px] uppercase tracking-widest text-muted font-semibold mb-2 flex items-center gap-2">
                <Navigation className="w-4 h-4" /> Routing Status
              </span>
              <span className={`text-2xl font-mono font-bold ${emergency.active ? 'text-warn' : 'text-primary'}`}>
                {emergency.active ? emergency.route.join(' → ') : 'STANDBY'}
              </span>
            </div>
            
            <div className="bg-panel border border-border-subtle rounded-lg p-4 flex flex-col items-center justify-center">
              <span className="text-[11px] uppercase tracking-widest text-muted font-semibold mb-2 flex items-center gap-2">
                <Clock className="w-4 h-4" /> Optimized ETA
              </span>
              <div className="flex items-baseline space-x-1">
                <span className={`text-4xl font-mono font-bold ${emergency.active ? 'text-warn' : 'text-primary'}`}>
                  {emergency.active ? eta : '--'}
                </span>
                <span className="text-sm font-mono text-muted">min</span>
              </div>
            </div>
          </div>

          {/* Network Map */}
          <div className="bg-panel border border-border-subtle rounded-lg p-4 flex-1 flex flex-col min-h-0">
            <h2 className="text-[11px] uppercase tracking-widest text-muted font-semibold mb-4 shrink-0">Live Enforcement Map</h2>
            <div className="flex-1 min-h-0 flex items-center justify-center">
               <TrafficNetwork />
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default EmergencyCorridor;
