// src/data/comparison.js

// Classical vs Hybrid optimization comparison metrics (Simulated Estimates)

export const pctChange = (before, after) => {
  if (before === 0) return 0;
  return Math.round(((after - before) / before) * 100);
};

export const COMPARISON_METRICS = [
  {
    label: "Avg Waiting Time",
    unit: "s",
    classical: 45,
    hybrid: 28,
    inverse: true, // lower is better
  },
  {
    label: "Total Queue Length",
    unit: "veh",
    classical: 120,
    hybrid: 85,
    inverse: true,
  },
  {
    label: "Network Throughput",
    unit: "veh/min",
    classical: 420,
    hybrid: 540,
    inverse: false, // higher is better
  },
  {
    label: "Estimated CO2",
    unit: "kg/h",
    classical: 85,
    hybrid: 62,
    inverse: true,
  },
  {
    label: "Fuel Consumption",
    unit: "gal/h",
    classical: 45,
    hybrid: 32,
    inverse: true,
  },
  {
    label: "Emergency ETA",
    unit: "min",
    classical: 18,
    hybrid: 11,
    inverse: true,
  }
];
