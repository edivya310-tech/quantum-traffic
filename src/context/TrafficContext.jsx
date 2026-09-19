import React, { createContext, useContext, useState, useEffect, useMemo, useCallback } from 'react';
import { getNetworkState } from '../utils/api';
import { calculateKPIs } from '../utils/metrics';

const TrafficContext = createContext(null);

export const TrafficProvider = ({ children }) => {
  const [intersections, setIntersections] = useState([]);
  const [initialSnapshot, setInitialSnapshot] = useState([]);
  
  const [emergency, setEmergency] = useState({
    active: false,
    route: [],
    log: [],
    origin: null,
    destination: null,
    preEmergencyState: null // For restoring state after deactivation
  });

  const [lastOptimization, setLastOptimization] = useState(null);
  const [scenarioState, setScenarioState] = useState(null);
  
  const [isLoading, setIsLoading] = useState(true);

  // Initialize network
  const initNetwork = useCallback(async () => {
    setIsLoading(true);
    const data = await getNetworkState();
    setIntersections(data);
    setInitialSnapshot(JSON.parse(JSON.stringify(data)));
    setIsLoading(false);
  }, []);

  useEffect(() => {
    initNetwork();
  }, [initNetwork]);

  const kpis = useMemo(() => {
    if (intersections.length === 0) return null;
    return calculateKPIs(intersections, emergency.active);
  }, [intersections, emergency.active]);

  const applyOptimizedPlan = useCallback((plan) => {
    // plan is array of { id, delta }
    setIntersections(prev => {
      const next = JSON.parse(JSON.stringify(prev));
      plan.forEach(p => {
        const intersection = next.find(i => i.id === p.id);
        if (intersection) {
          intersection.greenDuration += p.delta;
          // Apply some heuristic improvements to queue/waiting based on delta
          if (p.delta > 0) {
            intersection.queue = Math.max(0, intersection.queue - Math.floor(p.delta * 0.5));
            intersection.waiting = Math.max(0, intersection.waiting - p.delta);
            intersection.throughput += Math.floor(p.delta * 0.2);
          }
        }
      });
      return next;
    });
    setLastOptimization({
      timestamp: new Date().toISOString(),
      plan
    });
  }, []);

  const activateEmergencyRoute = useCallback((routeData) => {
    setEmergency(prev => ({
      ...prev,
      active: true,
      route: routeData.route,
      log: routeData.log,
      origin: routeData.origin,
      destination: routeData.destination,
      preEmergencyState: JSON.parse(JSON.stringify(intersections))
    }));

    // Preempt signals along route
    setIntersections(prev => {
      const next = JSON.parse(JSON.stringify(prev));
      routeData.route.forEach(nodeId => {
        const intersection = next.find(i => i.id === nodeId);
        if (intersection) {
          intersection.signal = 'GREEN';
          intersection.queue = Math.max(0, intersection.queue - 5);
        }
      });
      return next;
    });
  }, [intersections]);

  const deactivateEmergency = useCallback(() => {
    if (emergency.preEmergencyState) {
      setIntersections(emergency.preEmergencyState);
    }
    setEmergency({
      active: false,
      route: [],
      log: [],
      origin: null,
      destination: null,
      preEmergencyState: null
    });
  }, [emergency]);

  const applyScenarioImpact = useCallback((impactedState, config) => {
    setIntersections(impactedState);
    setScenarioState({
      config,
      status: 'impacted',
      timestamp: new Date().toISOString()
    });
  }, []);

  const applyScenarioOptimization = useCallback((optimizedState) => {
    setIntersections(optimizedState);
    setScenarioState(prev => ({
      ...prev,
      status: 'optimized'
    }));
  }, []);

  const resetNetwork = useCallback(() => {
    if (initialSnapshot.length > 0) {
      setIntersections(JSON.parse(JSON.stringify(initialSnapshot)));
    }
    setEmergency({ active: false, route: [], log: [], origin: null, destination: null, preEmergencyState: null });
    setLastOptimization(null);
    setScenarioState(null);
  }, [initialSnapshot]);

  return (
    <TrafficContext.Provider value={{
      intersections,
      kpis,
      emergency,
      lastOptimization,
      scenarioState,
      isLoading,
      applyOptimizedPlan,
      activateEmergencyRoute,
      deactivateEmergency,
      applyScenarioImpact,
      applyScenarioOptimization,
      resetNetwork,
      refresh: initNetwork
    }}>
      {children}
    </TrafficContext.Provider>
  );
};

export const useTraffic = () => useContext(TrafficContext);
