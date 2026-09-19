import React, { useState } from 'react';
import { cn } from '../utils/format';
import {
  Activity, Cpu, Zap, Radio, AlertTriangle, ShieldAlert,
  Leaf, GitFork, ArrowRight, Database, RefreshCcw, Car, ArrowDown, Network
} from 'lucide-react';
import { Link } from 'react-router-dom';

const InfoPanel = ({ title, content, isVisible, x, y }) => {
  if (!isVisible) return null;
  return (
    <div 
      className="fixed z-[100] bg-base/95 backdrop-blur-md border border-cyan/50 rounded-lg p-4 w-64 shadow-[0_0_20px_rgba(34,211,238,0.15)] pointer-events-none transform -translate-x-1/2 -translate-y-[120%]"
      style={{ left: x, top: y }}
    >
      <h4 className="text-cyan font-mono text-xs font-bold mb-2 uppercase">{title}</h4>
      <p className="text-sm text-secondary">{content}</p>
    </div>
  );
};

const StageLabel = ({ num, text }) => (
  <div className="flex items-center gap-2 mb-4">
    <span className="font-mono text-xs font-bold text-muted bg-elevated px-2 py-1 rounded border border-border-strong">{num}</span>
    <span className="font-mono text-xs font-bold tracking-widest uppercase text-secondary">{text}</span>
  </div>
);

const FlowArrow = ({ color = "text-border-strong", glow = false }) => (
  <div className="flex flex-col items-center justify-center py-2 opacity-60 z-0 relative">
     <div className={cn("w-px h-10 border-l-2 border-dashed", `border-${color.replace('text-', '')}`)}></div>
     <ArrowDown className={cn("w-5 h-5 -mt-2", color, glow && "drop-shadow-[0_0_8px_currentColor]")} />
  </div>
);

const SystemArchitecture = () => {
  const [activeInfo, setActiveInfo] = useState(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e) => {
    setMousePos({ x: e.clientX, y: e.clientY });
  };

  const setHoverInfo = (info) => {
    setActiveInfo(info);
  };

  const clearHoverInfo = () => {
    setActiveInfo(null);
  };

  return (
    <div 
      className="flex flex-col h-full bg-void text-primary font-sans overflow-hidden relative selection:bg-cyan selection:text-void"
      onMouseMove={handleMouseMove}
    >
      {/* Background Technical Grid */}
      <div className="absolute inset-0 pointer-events-none opacity-5 z-0"
        style={{
          backgroundImage: 'linear-gradient(#37455f 1px, transparent 1px), linear-gradient(90deg, #37455f 1px, transparent 1px)',
          backgroundSize: '40px 40px'
        }}
      />

      <InfoPanel 
        title={activeInfo?.title} 
        content={activeInfo?.content} 
        isVisible={!!activeInfo}
        x={mousePos.x}
        y={mousePos.y}
      />

      {/* HEADER */}
      <header className="shrink-0 p-6 lg:p-8 flex flex-col md:flex-row md:items-start justify-between z-10 border-b border-border-subtle bg-base/80 backdrop-blur-md">
        <div>
          <h1 className="text-2xl md:text-4xl font-bold tracking-tight text-primary flex items-center gap-3">
            <RefreshCcw className="text-cyan w-8 h-8" />
            Q-TRAFFIC INTELLIGENCE LOOP
          </h1>
          <p className="text-secondary mt-2 text-sm md:text-base max-w-2xl">
            Real-time traffic intelligence → prediction → quantum optimization → signal control → continuous feedback
          </p>
        </div>
        
        <div className="mt-4 md:mt-0 flex flex-col items-end gap-3">
          <div className="flex items-center space-x-2 bg-cyan/10 text-cyan px-4 py-2 rounded border border-cyan/30 shadow-[0_0_15px_rgba(34,211,238,0.2)]">
            <div className="w-2.5 h-2.5 rounded-full bg-cyan animate-pulse" />
            <span className="font-mono font-bold tracking-widest uppercase text-xs">● OPTIMIZATION ENGINE ONLINE</span>
          </div>
          <div className="flex gap-4 text-[10px] font-mono uppercase tracking-widest text-muted">
            <span>8 Intersections</span>
            <span>24 Signal Phases</span>
            <span>Real-Time Analysis</span>
            <span>Hybrid Optimization</span>
          </div>
        </div>
      </header>

      {/* MAIN CONTENT AREA */}
      <div className="flex-1 overflow-y-auto overflow-x-hidden relative p-8">
        <div className="max-w-5xl mx-auto flex flex-col items-center relative py-6 w-full">
          
          {/* THE LOOP SVG BORDER (Stage 6 -> Stage 2) */}
          <div className="absolute hidden lg:block left-0 xl:-left-12 top-[240px] bottom-[150px] w-24 border-l-2 border-t-2 border-b-2 border-dashed border-teal-500/30 rounded-l-3xl pointer-events-none z-0">
             {/* Upward Arrow on the feedback loop */}
             <div className="absolute -left-[11px] top-1/2 bg-void p-1 rounded-full">
               <ArrowDown className="w-4 h-4 text-teal-500 rotate-180" />
             </div>
          </div>

          {/* STAGE 1: DATA INGESTION */}
          <div className="flex flex-col items-center w-full z-10 relative">
            <StageLabel num="01" text="Data Ingestion" />
            <div className="flex justify-center gap-6 w-full max-w-[600px]">
              {/* SCATS LIVE FEED */}
              <Link 
                to="/command-center"
                className="flex-1 bg-panel/95 backdrop-blur-sm border border-cyan/30 rounded-xl p-5 hover:border-cyan hover:bg-elevated transition-all flex flex-col items-center text-center shadow-[0_0_15px_rgba(34,211,238,0.05)] group"
                onMouseEnter={() => setHoverInfo({ title: 'SCATS Live Feed', content: 'Real-time intersection state capture' })}
                onMouseLeave={clearHoverInfo}
              >
                <Radio className="w-6 h-6 text-cyan mb-3 group-hover:scale-110 transition-transform" />
                <h3 className="font-bold text-sm mb-1">SCATS LIVE FEED</h3>
                <p className="text-xs text-secondary">Real-time intersection state</p>
              </Link>
              
              {/* SCENARIO ENGINE */}
              <Link 
                to="/scenario"
                className="flex-1 bg-panel/95 backdrop-blur-sm border border-cyan/30 border-dashed rounded-xl p-5 hover:border-cyan hover:bg-elevated transition-all flex flex-col items-center text-center shadow-[0_0_15px_rgba(34,211,238,0.05)] group"
                onMouseEnter={() => setHoverInfo({ title: 'Scenario Engine', content: 'Simulated anomalies & stress testing' })}
                onMouseLeave={clearHoverInfo}
              >
                <Cpu className="w-6 h-6 text-cyan mb-3 group-hover:scale-110 transition-transform" />
                <h3 className="font-bold text-sm mb-1">SCENARIO ENGINE</h3>
                <p className="text-xs text-secondary">Simulated anomalies & stress testing</p>
              </Link>
            </div>
          </div>

          {/* Connection 1 to 2 */}
          <div className="flex w-full max-w-[600px] justify-center relative">
             <div className="absolute top-0 w-1/2 h-px bg-dashed border-t-2 border-dashed border-border-strong mt-2"></div>
             <FlowArrow color="text-cyan" />
          </div>

          {/* STAGE 2: INTELLIGENCE LAYER */}
          <div className="flex flex-col items-center w-full z-10 relative">
            <StageLabel num="02" text="Intelligence" />
            <div 
              className="w-full max-w-[600px] bg-panel/95 backdrop-blur-sm border border-cyan/50 rounded-xl p-6 shadow-[0_0_20px_rgba(34,211,238,0.1)] group hover:border-cyan hover:shadow-[0_0_30px_rgba(34,211,238,0.2)] transition-all flex flex-col items-center relative"
              onMouseEnter={() => setHoverInfo({ title: 'Intelligence Core', content: 'AI processing of raw data into predictive traffic models.' })}
              onMouseLeave={clearHoverInfo}
            >
              <h3 className="text-cyan font-mono font-bold tracking-widest uppercase flex items-center gap-2 mb-6"><Cpu className="w-5 h-5"/> INTELLIGENCE CORE</h3>
              
              <div className="flex flex-col gap-3 w-full max-w-[400px] items-center font-mono text-sm relative z-10">
                 <div className="w-full text-center py-2 bg-base/80 border border-border-strong rounded flex items-center justify-center gap-2">
                    <Car className="w-4 h-4 text-cyan" /> TRAFFIC STATE
                 </div>
                 <ArrowDown className="w-4 h-4 text-cyan" />
                 <div className="w-full text-center py-2 bg-base/80 border border-border-strong rounded flex items-center justify-center gap-2">
                    <Activity className="w-4 h-4 text-cyan" /> CONGESTION PREDICTION
                 </div>
                 <ArrowDown className="w-4 h-4 text-cyan" />
                 <div className="w-full text-center py-2 bg-cyan/10 text-cyan border border-cyan/40 rounded flex items-center justify-center gap-2 font-bold shadow-[0_0_10px_rgba(34,211,238,0.2)]">
                    <Network className="w-4 h-4" /> MULTI-OBJECTIVE OPTIMIZATION
                 </div>
              </div>

              <div className="flex flex-wrap justify-center gap-2 mt-6 text-[10px] text-secondary font-mono">
                 <span className="px-2 py-1 bg-elevated rounded border border-border-subtle group-hover:border-cyan/30 transition-colors">Vehicle density</span>
                 <span className="px-2 py-1 bg-elevated rounded border border-border-subtle group-hover:border-cyan/30 transition-colors">Queue length</span>
                 <span className="px-2 py-1 bg-elevated rounded border border-border-subtle group-hover:border-cyan/30 transition-colors">Signal phase</span>
                 <span className="px-2 py-1 bg-elevated rounded border border-border-subtle group-hover:border-cyan/30 transition-colors">Travel time</span>
                 <span className="px-2 py-1 bg-elevated rounded border border-border-subtle group-hover:border-cyan/30 transition-colors">Emergency events</span>
              </div>
            </div>
          </div>

          <FlowArrow color="text-[#8b5cf6]" />

          {/* STAGE 3: QUANTUM FORMULATION */}
          <div className="flex flex-col items-center w-full z-10 relative">
            <StageLabel num="03" text="Formulation" />
            <Link 
              to="/optimizer"
              className="w-full max-w-[600px] bg-panel/95 backdrop-blur-sm border border-[#8b5cf6]/50 rounded-xl p-6 shadow-[0_0_20px_rgba(139,92,246,0.15)] group hover:border-[#8b5cf6] hover:shadow-[0_0_30px_rgba(139,92,246,0.3)] transition-all flex flex-col items-center cursor-pointer"
              onMouseEnter={() => setHoverInfo({ title: 'QUBO Formulation', content: 'Translating traffic objectives into a Quadratic Unconstrained Binary Optimization model.' })}
              onMouseLeave={clearHoverInfo}
            >
              <h3 className="text-[#8b5cf6] font-mono font-bold tracking-widest uppercase flex items-center gap-2 mb-2"><Zap className="w-5 h-5"/> QUBO FORMULATION</h3>
              <p className="text-xs text-[#8b5cf6]/70 mb-5 text-center font-mono">"Translate traffic state into optimization variables"</p>
              
              <div className="flex items-center gap-2 md:gap-4 w-full justify-center text-xs font-mono">
                 <div className="px-2 md:px-4 py-2 bg-base/80 rounded border border-border-subtle text-secondary">Traffic State</div>
                 <ArrowRight className="w-4 h-4 text-muted" />
                 <div className="px-2 md:px-4 py-2 bg-base/80 rounded border border-border-subtle text-secondary">Binary Variables</div>
                 <ArrowRight className="w-4 h-4 text-muted" />
                 <div className="px-2 md:px-4 py-2 bg-[#8b5cf6]/10 text-[#8b5cf6] rounded border border-[#8b5cf6]/40 font-bold shadow-[0_0_10px_rgba(139,92,246,0.2)]">QUBO Matrix</div>
              </div>
            </Link>
          </div>

          <FlowArrow color="text-[#a855f7]" glow />

          {/* STAGE 4: QUANTUM SOLVER */}
          <div className="flex flex-col items-center w-full z-10 relative">
            <StageLabel num="04" text="Quantum Solver" />
            <Link 
              to="/optimizer"
              className="w-full max-w-[600px] bg-panel/95 backdrop-blur-sm border-2 border-[#a855f7]/80 rounded-xl p-6 shadow-[0_0_40px_rgba(168,85,247,0.25)] group hover:shadow-[0_0_60px_rgba(168,85,247,0.4)] transition-all relative overflow-hidden flex flex-col items-center cursor-pointer"
              onMouseEnter={() => setHoverInfo({ title: 'Quantum Core', content: 'Utilizes QAOA to find the global optimum.' })}
              onMouseLeave={clearHoverInfo}
            >
              {/* Internal glowing circuit effect */}
              <div className="absolute inset-0 pointer-events-none opacity-20 bg-gradient-to-b from-[#a855f7]/10 to-transparent" />
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-[#a855f7] to-transparent opacity-50" />
              
              <h3 className="text-[#e9d5ff] font-mono font-bold tracking-widest uppercase flex items-center gap-2 mb-6 relative z-10 drop-shadow-[0_0_5px_rgba(168,85,247,0.8)]"><Database className="w-5 h-5"/> QUANTUM CORE</h3>
              
              <div className="flex flex-col items-center gap-3 w-full max-w-[400px] relative z-10 font-mono text-sm">
                <div className="w-full text-center py-2 bg-base/80 border border-border-strong rounded text-secondary">QUBO</div>
                <ArrowDown className="w-4 h-4 text-[#a855f7]" />
                <div className="w-full text-center py-3 bg-[#a855f7]/20 border border-[#a855f7] font-bold text-[#e9d5ff] rounded shadow-[0_0_15px_rgba(168,85,247,0.4)] relative overflow-hidden">
                  <div className="absolute inset-0 bg-white/5 animate-pulse" />
                  QAOA
                </div>
                <ArrowDown className="w-4 h-4 text-[#a855f7]" />
                <div className="w-full text-center py-2 bg-base/80 border border-border-strong rounded text-secondary">HYBRID SOLVER</div>
                <ArrowDown className="w-4 h-4 text-[#a855f7]" />
                <div className="w-full text-center py-2 bg-[#a855f7]/10 border border-[#a855f7]/40 text-[#d8b4fe] font-bold rounded">OPTIMAL SIGNAL PLAN</div>
              </div>
            </Link>
          </div>

          <div className="flex w-full max-w-[600px] justify-center relative">
             <div className="absolute top-[28px] w-[55%] h-px border-t-2 border-dashed border-border-strong" />
             <div className="absolute top-[28px] right-[22%] w-px h-[20px] border-l-2 border-dashed border-border-strong" />
             <div className="absolute top-[28px] left-[22%] w-px h-[20px] border-l-2 border-dashed border-border-strong" />
             <FlowArrow color="text-border-strong" />
          </div>

          {/* STAGE 5: CONTROL & SAFETY */}
          <div className="flex flex-col items-center w-full z-10 relative mt-4">
            <StageLabel num="05" text="Control" />
            <div className="flex flex-col md:flex-row justify-center gap-6 w-full max-w-[700px]">
              
              {/* SIGNAL CONTROL */}
              <div 
                className="flex-1 bg-panel/95 backdrop-blur-sm border border-go/40 rounded-xl p-5 hover:border-go transition-colors shadow-[0_0_20px_rgba(34,197,94,0.05)] hover:shadow-[0_0_30px_rgba(34,197,94,0.2)] flex flex-col items-center text-center group"
                onMouseEnter={() => setHoverInfo({ title: 'Signal Control', content: 'Applying optimized green splits and offsets to field controllers.' })}
                onMouseLeave={clearHoverInfo}
              >
                <div className="w-12 h-12 rounded-full bg-go/10 flex items-center justify-center mb-4 group-hover:bg-go/20 transition-colors border border-go/20">
                  <GitFork className="w-6 h-6 text-go" />
                </div>
                <h3 className="font-bold text-sm mb-3 text-primary">SIGNAL CONTROL</h3>
                <div className="bg-base/80 border border-border-subtle rounded w-full py-2 mb-2 text-xs font-mono text-secondary">Optimized traffic phases</div>
                <div className="bg-base/80 border border-border-subtle rounded w-full py-2 text-xs font-mono text-secondary">Green-wave coordination</div>
              </div>
              
              {/* EMERGENCY OVERRIDE */}
              <Link 
                to="/emergency"
                className="flex-1 bg-panel/95 backdrop-blur-sm border border-warn/40 rounded-xl p-5 hover:border-warn transition-colors shadow-[0_0_20px_rgba(234,179,8,0.05)] hover:shadow-[0_0_30px_rgba(234,179,8,0.2)] flex flex-col items-center text-center group cursor-pointer"
                onMouseEnter={() => setHoverInfo({ title: 'Emergency Override', content: 'Bypasses standard optimization for immediate path clearing.' })}
                onMouseLeave={clearHoverInfo}
              >
                <div className="w-12 h-12 rounded-full bg-warn/10 flex items-center justify-center mb-4 group-hover:bg-warn/20 transition-colors border border-warn/20">
                  <ShieldAlert className="w-6 h-6 text-warn" />
                </div>
                <h3 className="font-bold text-sm mb-3 text-primary">EMERGENCY OVERRIDE</h3>
                <div className="bg-base/80 border border-border-subtle rounded w-full py-2 mb-2 text-xs font-mono text-secondary">Emergency vehicle priority</div>
                <div className="bg-base/80 border border-border-subtle rounded w-full py-2 text-xs font-mono text-secondary">Pre-emptive green-wave routing</div>
              </Link>

            </div>
          </div>

          <div className="flex w-full max-w-[700px] justify-center relative mt-4">
             <div className="absolute top-0 w-[55%] h-px border-t-2 border-dashed border-border-strong mt-2" />
             <FlowArrow color="text-teal-500" />
          </div>

          {/* STAGE 6: FEEDBACK LOOP */}
          <div className="flex flex-col items-center w-full z-10 relative">
            <StageLabel num="06" text="Feedback" />
            <Link 
              to="/environment"
              className="w-full max-w-[600px] bg-panel/95 backdrop-blur-sm border border-teal-500/40 rounded-xl p-6 hover:border-teal-500 shadow-[0_0_20px_rgba(20,184,166,0.1)] hover:shadow-[0_0_30px_rgba(20,184,166,0.25)] transition-colors flex flex-col items-center cursor-pointer"
              onMouseEnter={() => setHoverInfo({ title: 'Sustainability', content: 'Continuous monitoring of environmental and efficiency KPIs.' })}
              onMouseLeave={clearHoverInfo}
            >
              <h3 className="text-teal-400 font-mono font-bold tracking-widest uppercase flex items-center gap-2 mb-5"><Leaf className="w-5 h-5"/> SUSTAINABILITY + FEEDBACK</h3>
              
              <div className="grid grid-cols-2 sm:grid-cols-4 w-full text-xs font-mono text-secondary gap-3">
                 <div className="bg-base/80 p-2 border border-border-subtle rounded text-center flex flex-col items-center gap-1">Fuel <ArrowDown className="w-4 h-4 text-go" /></div>
                 <div className="bg-base/80 p-2 border border-border-subtle rounded text-center flex flex-col items-center gap-1">CO₂ <ArrowDown className="w-4 h-4 text-go" /></div>
                 <div className="bg-base/80 p-2 border border-border-subtle rounded text-center flex flex-col items-center gap-1">Waiting Time <ArrowDown className="w-4 h-4 text-go" /></div>
                 <div className="bg-base/80 p-2 border border-border-subtle rounded text-center flex flex-col items-center gap-1">Congestion <ArrowDown className="w-4 h-4 text-go" /></div>
              </div>
            </Link>
          </div>

        </div>
      </div>

      {/* FOOTER LEGEND */}
      <footer className="shrink-0 bg-base border-t border-border-subtle p-4 flex justify-center z-10">
        <div className="flex flex-wrap justify-center gap-4 md:gap-8 text-[10px] font-mono tracking-widest uppercase">
           <span className="flex items-center gap-2 text-cyan"><div className="w-1.5 h-1.5 rounded-full bg-cyan" /> DATA</span>
           <span className="flex items-center gap-2 text-cyan"><div className="w-1.5 h-1.5 rounded-full bg-cyan" /> AI PREDICTION</span>
           <span className="flex items-center gap-2 text-[#8b5cf6]"><div className="w-1.5 h-1.5 rounded-full bg-[#8b5cf6]" /> QUBO</span>
           <span className="flex items-center gap-2 text-[#a855f7]"><div className="w-1.5 h-1.5 rounded-full bg-[#a855f7] animate-pulse" /> QAOA</span>
           <span className="flex items-center gap-2 text-go"><div className="w-1.5 h-1.5 rounded-full bg-go" /> SIGNAL CONTROL</span>
           <span className="flex items-center gap-2 text-teal-400"><div className="w-1.5 h-1.5 rounded-full bg-teal-400" /> ENVIRONMENT</span>
        </div>
      </footer>
      
    </div>
  );
};

export default SystemArchitecture;
