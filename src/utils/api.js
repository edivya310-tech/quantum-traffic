// src/utils/api.js

// Mock Data
const INITIAL_INTERSECTIONS = [
  { id: 'I1', density: 0.3, queue: 12, capacity: 60, signal: 'GREEN', greenDuration: 45, redDuration: 45, waiting: 20, throughput: 45 },
  { id: 'I2', density: 0.8, queue: 45, capacity: 60, signal: 'RED', greenDuration: 30, redDuration: 60, waiting: 85, throughput: 30 },
  { id: 'I3', density: 0.2, queue: 5, capacity: 50, signal: 'GREEN', greenDuration: 45, redDuration: 45, waiting: 10, throughput: 35 },
  { id: 'I4', density: 0.9, queue: 55, capacity: 70, signal: 'RED', greenDuration: 25, redDuration: 65, waiting: 120, throughput: 20 },
  { id: 'I5', density: 0.4, queue: 15, capacity: 60, signal: 'YELLOW', greenDuration: 40, redDuration: 50, waiting: 25, throughput: 40 },
  { id: 'I6', density: 0.6, queue: 28, capacity: 60, signal: 'GREEN', greenDuration: 50, redDuration: 40, waiting: 45, throughput: 50 },
  { id: 'I7', density: 0.7, queue: 35, capacity: 80, signal: 'RED', greenDuration: 35, redDuration: 55, waiting: 60, throughput: 35 },
  { id: 'I8', density: 0.1, queue: 2, capacity: 50, signal: 'GREEN', greenDuration: 60, redDuration: 30, waiting: 5, throughput: 40 },
];

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export const getNetworkState = async () => {
  await delay(300);
  // Return deep copy
  return JSON.parse(JSON.stringify(INITIAL_INTERSECTIONS));
};

export const runOptimization = async (state) => {
  await delay(1500); // Simulate quantum processing time
  
  return state.map(i => {
    // Generate a mock optimization delta based on current density
    let delta = 0;
    if (i.density > 0.7) delta = Math.floor(Math.random() * 15) + 5; // Increase green
    else if (i.density < 0.3) delta = -(Math.floor(Math.random() * 10) + 2); // Decrease green
    
    return {
      id: i.id,
      before: i.greenDuration,
      after: i.greenDuration + delta,
      delta: delta,
    };
  });
};

export const activateEmergency = async ({ origin, destination }) => {
  await delay(500);
  // Mock routing
  const allNodes = ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8'];
  // Simple mock route: just pick 3-4 nodes between origin and destination
  const route = [origin];
  const possibleMidpoints = allNodes.filter(n => n !== origin && n !== destination);
  route.push(possibleMidpoints[Math.floor(Math.random() * possibleMidpoints.length)]);
  if (Math.random() > 0.5) {
    route.push(possibleMidpoints[Math.floor(Math.random() * possibleMidpoints.length)]);
  }
  route.push(destination);
  
  // Deduplicate route
  const uniqueRoute = [...new Set(route)];

  return {
    route: uniqueRoute,
    log: [
      { timestamp: new Date().toISOString(), message: `Emergency requested from ${origin} to ${destination}` },
      { timestamp: new Date().toISOString(), message: `Quantum routing optimizing path...` },
      { timestamp: new Date().toISOString(), message: `Corridor established via ${uniqueRoute.join(' -> ')}` },
      { timestamp: new Date().toISOString(), message: `Pre-empting signals along route...` }
    ]
  };
};

export const runScenario = async (config) => {
  await delay(1000);
  
  // Create an impacted state
  const impacted = JSON.parse(JSON.stringify(INITIAL_INTERSECTIONS)).map(i => {
    // Apply impact
    if (i.id === config.location) {
      i.density = Math.min(1.0, i.density + (config.intensity / 100));
      i.queue += Math.floor(config.intensity * 0.8);
      i.waiting += config.intensity * 2;
      i.throughput = Math.max(0, i.throughput - (config.intensity * 0.5));
      i.signal = 'RED'; // Often goes red or clogged in accident
    }
    return i;
  });

  // Create an optimized response state
  const optimized = JSON.parse(JSON.stringify(impacted)).map(i => {
    if (i.id === config.location) {
      i.queue = Math.floor(i.queue * 0.6); // 40% reduction
      i.waiting = Math.floor(i.waiting * 0.5); // 50% reduction
      i.throughput += 15;
      i.signal = 'GREEN';
    } else {
      // Small improvements everywhere else
      i.queue = Math.max(0, i.queue - 2);
    }
    return i;
  });

  return {
    impact: impacted,
    optimized: optimized
  };
};

export const getEnvironmentTimeseries = async () => {
  await delay(200);
  
  const data = [];
  let time = 0;
  for(let i=0; i<20; i++) {
    data.push({
      time: `${time}m`,
      baselineCO2: 100 + Math.random() * 20,
      hybridCO2: 70 + Math.random() * 15,
      baselineFuel: 50 + Math.random() * 10,
      hybridFuel: 35 + Math.random() * 8,
    });
    time += 5;
  }
  return data;
};

export const getComparisonSummary = async () => {
  await delay(200);
  const { COMPARISON_METRICS } = await import('../data/comparison.js');
  return COMPARISON_METRICS;
};
