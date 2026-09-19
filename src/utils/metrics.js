// src/utils/metrics.js

// Derived KPI calculations based on intersections state
export const calculateKPIs = (intersections, emergencyActive = false) => {
  const totalQueue = intersections.reduce((sum, i) => sum + i.queue, 0);
  const avgWaiting = Math.round(intersections.reduce((sum, i) => sum + i.waiting, 0) / intersections.length);
  const totalThroughput = intersections.reduce((sum, i) => sum + i.throughput, 0);
  
  // Simulated estimates based on queue and waiting
  const estimatedCO2 = Math.round((totalQueue * 0.5) + (avgWaiting * 0.2)); // kg/h
  const estimatedFuel = Math.round((totalQueue * 0.1) + (avgWaiting * 0.05)); // gal/h
  
  // Emergency ETA based on network density
  const baseETA = 15; // mins
  const etaPenalty = emergencyActive ? 0 : Math.round(totalQueue / 10);
  const currentETA = baseETA + etaPenalty;

  return {
    queue: totalQueue,
    waiting: avgWaiting,
    throughput: totalThroughput,
    co2: estimatedCO2,
    fuel: estimatedFuel,
    emergencyETA: currentETA,
  };
};

export const calculateHealthScore = (kpis) => {
  // Simple heuristic: 100 is perfect, degrades with higher queues and waiting, improves with throughput
  const base = 100;
  const queuePenalty = Math.min(kpis.queue * 0.5, 40);
  const waitingPenalty = Math.min(kpis.waiting * 0.2, 40);
  const throughputBonus = Math.min(kpis.throughput * 0.05, 20);
  
  const score = base - queuePenalty - waitingPenalty + throughputBonus;
  return Math.max(0, Math.min(100, Math.round(score)));
};

export const generatePredictiveCongestion = (intersections) => {
  // Generate 15-minute forecast sparkline points
  const points = [];
  const baseCongestion = intersections.reduce((sum, i) => sum + i.density, 0) / intersections.length;
  
  for (let i = 0; i < 15; i++) {
    // Add some random walk for trend
    const trend = (Math.random() - 0.4) * 0.1;
    points.push({
      time: `+${i}m`,
      value: Math.max(0, Math.min(1, baseCongestion + trend * i))
    });
  }
  return points;
};
