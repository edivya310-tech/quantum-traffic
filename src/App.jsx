import React from 'react';
import { Routes, Route, Outlet } from 'react-router-dom';
import Shell from './components/Shell';
import LandingPage from './pages/LandingPage';
import CommandCenter from './pages/CommandCenter';
import QuantumOptimizer from './pages/QuantumOptimizer';
import EmergencyCorridor from './pages/EmergencyCorridor';
import ScenarioSimulator from './pages/ScenarioSimulator';
import Environment from './pages/Environment';
import ClassicalVsHybrid from './pages/ClassicalVsHybrid';
import SystemArchitecture from './pages/SystemArchitecture';

const ShellWrapper = () => (
  <Shell>
    <Outlet />
  </Shell>
);

function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route element={<ShellWrapper />}>
        <Route path="/command-center" element={<CommandCenter />} />
        <Route path="/optimizer" element={<QuantumOptimizer />} />
        <Route path="/emergency" element={<EmergencyCorridor />} />
        <Route path="/scenario" element={<ScenarioSimulator />} />
        <Route path="/environment" element={<Environment />} />
        <Route path="/comparison" element={<ClassicalVsHybrid />} />
        <Route path="/architecture" element={<SystemArchitecture />} />
      </Route>
    </Routes>
  );
}

export default App;
