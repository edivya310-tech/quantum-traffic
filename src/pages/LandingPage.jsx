import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Activity, Network, Zap, Route } from 'lucide-react';

const EXPLORE_OPTIONS = [
  {
    id: 'flow',
    icon: Activity,
    title: 'Traffic Flow',
    description: 'Analyze congestion and movement patterns across the network.'
  },
  {
    id: 'intelligence',
    icon: Network,
    title: 'Network Intelligence',
    description: 'Understand relationships between traffic conditions across locations.'
  },
  {
    id: 'optimization',
    icon: Route,
    title: 'Route Optimization',
    description: 'Explore efficient movement patterns and traffic-aware routing.'
  },
  {
    id: 'insights',
    icon: Zap,
    title: 'Predictive Insights',
    description: 'Explore potential traffic conditions and mobility patterns.'
  }
];

const LandingPage = () => {
  const [selectedOption, setSelectedOption] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const navigate = useNavigate();

  const handleLaunch = () => {
    if (!selectedOption) return;
    
    setIsAnalyzing(true);
    
    // Simulate short initialization delay
    setTimeout(() => {
      navigate('/command-center');
    }, 1500);
  };

  return (
    <div className="relative min-h-screen bg-void text-primary font-sans overflow-hidden quantum-bg flex flex-col justify-center items-center">
      
      {/* Background Elements */}
      <div className="absolute inset-0 z-0 opacity-30 grid-bg animate-grid-move"></div>
      
      {/* Abstract Quantum Particles */}
      <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-32 h-32 bg-cyan/20 rounded-full blur-3xl animate-particle-1"></div>
        <div className="absolute top-2/3 right-1/4 w-40 h-40 bg-indigo-500/20 rounded-full blur-3xl animate-particle-2"></div>
        <div className="absolute top-1/2 left-1/2 w-48 h-48 bg-purple-500/10 rounded-full blur-3xl animate-particle-3"></div>
      </div>

      {/* Main Content */}
      <div className="relative z-10 w-full max-w-7xl px-6 lg:px-12 grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center animate-fade-in py-12">
        
        {/* Left Column: Text and Selection */}
        <div className="flex flex-col space-y-8">
          
          <div className="space-y-4">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full border border-cyan/30 bg-cyan/10 text-cyan text-xs font-mono tracking-wider">
              <Zap className="w-3 h-3" />
              <span>QUANTUM CORE ACTIVE</span>
            </div>
            
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight text-white leading-tight">
              QUANTUM TRAFFIC <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan to-indigo-400">INTELLIGENCE</span>
            </h1>
            
            <p className="text-secondary text-lg max-w-md">
              Smarter mobility through quantum-inspired intelligence. Analyze real-time conditions, optimize routes, and support intelligent mobility decisions at a macro scale.
            </p>
          </div>

          <div className="space-y-4 pt-4">
            <h3 className="text-sm font-mono text-cyan tracking-wider uppercase">What would you like to explore?</h3>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {EXPLORE_OPTIONS.map((option) => (
                <button
                  key={option.id}
                  type="button"
                  onClick={() => setSelectedOption(option.id)}
                  className={`relative text-left p-4 rounded-xl border transition-all duration-300 overflow-hidden group ${
                    selectedOption === option.id 
                      ? 'bg-cyan/10 border-cyan shadow-[0_0_15px_rgba(34,211,238,0.2)]' 
                      : 'bg-elevated/40 border-border-strong hover:border-cyan/50 hover:bg-elevated/60 backdrop-blur-md'
                  }`}
                >
                  <div className={`absolute top-0 left-0 w-1 h-full transition-colors duration-300 ${selectedOption === option.id ? 'bg-cyan' : 'bg-transparent group-hover:bg-cyan/30'}`}></div>
                  <div className="flex items-start space-x-3">
                    <option.icon className={`w-5 h-5 mt-0.5 flex-shrink-0 transition-colors duration-300 ${selectedOption === option.id ? 'text-cyan' : 'text-secondary group-hover:text-cyan/70'}`} />
                    <div>
                      <h4 className={`text-sm font-semibold mb-1 transition-colors duration-300 ${selectedOption === option.id ? 'text-primary' : 'text-primary/90'}`}>
                        {option.title}
                      </h4>
                      <p className="text-xs text-muted leading-relaxed">
                        {option.description}
                      </p>
                    </div>
                  </div>
                </button>
              ))}
            </div>

            <button
              onClick={handleLaunch}
              disabled={isAnalyzing || !selectedOption}
              className="w-full mt-6 bg-cyan/20 hover:bg-cyan/30 border border-cyan/50 text-cyan py-4 rounded-xl font-mono text-sm tracking-wider uppercase transition-all duration-300 flex items-center justify-center space-x-2 animate-glow disabled:opacity-50 disabled:cursor-not-allowed disabled:animate-none"
            >
              {isAnalyzing ? (
                <>
                  <Activity className="w-5 h-5 animate-spin" />
                  <span>Initializing Systems...</span>
                </>
              ) : (
                <>
                  <span>Launch Traffic Intelligence</span>
                  <span className="text-lg leading-none">→</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Right Column: Visual Elements */}
        <div className="hidden lg:flex justify-center items-center relative animate-float">
          {/* Main glowing sphere/node */}
          <div className="w-[300px] h-[300px] xl:w-[400px] xl:h-[400px] rounded-full border border-cyan/20 relative flex items-center justify-center before:absolute before:inset-0 before:rounded-full before:bg-cyan/5 before:blur-2xl">
            
            <div className="w-[200px] h-[200px] xl:w-[260px] xl:h-[260px] rounded-full border border-cyan/30 animate-pulse-slow flex items-center justify-center">
              <div className="w-[120px] h-[120px] xl:w-[160px] xl:h-[160px] rounded-full border border-cyan/50 flex items-center justify-center bg-cyan/10">
                <Network className="w-16 h-16 xl:w-20 xl:h-20 text-cyan drop-shadow-[0_0_12px_rgba(34,211,238,0.9)]" />
              </div>
            </div>

            {/* Orbiting nodes */}
            <div className="absolute w-full h-full animate-[spin_12s_linear_infinite]">
              <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-4 h-4 bg-cyan rounded-full shadow-[0_0_15px_#22d3ee]"></div>
              <div className="absolute bottom-1/4 right-0 translate-x-1/2 translate-y-1/2 w-2 h-2 bg-cyan/60 rounded-full shadow-[0_0_8px_#22d3ee]"></div>
            </div>
            <div className="absolute w-full h-full animate-[spin_18s_linear_infinite_reverse]">
              <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-1/2 w-3 h-3 bg-indigo-400 rounded-full shadow-[0_0_12px_#818cf8]"></div>
              <div className="absolute top-1/4 left-0 -translate-x-1/2 -translate-y-1/2 w-2.5 h-2.5 bg-indigo-500 rounded-full shadow-[0_0_10px_#6366f1]"></div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Status Indicators */}
      <div className="absolute bottom-6 left-0 right-0 flex justify-center items-center animate-fade-in" style={{ animationDelay: '0.5s' }}>
        <div className="flex flex-col md:flex-row items-center space-y-3 md:space-y-0 md:space-x-8 text-xs font-mono tracking-widest text-muted">
          
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 rounded-full bg-go animate-pulse-slow shadow-[0_0_5px_#22c55e]"></div>
            <span>AI Engine Online</span>
          </div>

          <div className="hidden md:block w-1 h-1 rounded-full bg-border-strong"></div>

          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 rounded-full bg-cyan animate-pulse-slow shadow-[0_0_5px_#22d3ee]" style={{ animationDelay: '1s' }}></div>
            <span>Quantum Optimization Ready</span>
          </div>

          <div className="hidden md:block w-1 h-1 rounded-full bg-border-strong"></div>

          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse-slow shadow-[0_0_5px_#818cf8]" style={{ animationDelay: '2s' }}></div>
            <span>Network-Wide Analysis Active</span>
          </div>
          
        </div>
      </div>

    </div>
  );
};

export default LandingPage;
