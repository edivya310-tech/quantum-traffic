# API Contract for Q-TRAFFIC

This document specifies the exact interface the frontend uses to interact with the backend (e.g. Python/FastAPI + Qiskit/QAOA).
The frontend is designed so that a real backend can be dropped in by modifying a single file: `src/utils/api.js`.

## Endpoints

### 1. Get Network State
`GET /api/network/state`
Returns the current state of all 8 intersections.
**Response**: `Intersection[]`
```typescript
type Intersection = {
  id: string; // e.g. "I1", "I2"
  density: number; // 0.0 to 1.0
  queue: number; // number of waiting vehicles
  capacity: number; // max vehicles per hour
  signal: 'GREEN' | 'RED' | 'YELLOW';
  greenDuration: number; // seconds
  redDuration: number; // seconds
  waiting: number; // total waiting time
  throughput: number; // vehicles passing per minute
}
```

### 2. Run Optimization
`POST /api/optimize/run`
**Request**: `{ state: Intersection[] }`
**Response**: `{ id: string, before: number, after: number, delta: number }[]`
Returns the proposed changes to the green light duration for each intersection.

### 3. Activate Emergency Corridor
`POST /api/emergency/activate`
**Request**: `{ origin: string, destination: string }`
**Response**: 
```typescript
{
  route: string[]; // e.g. ["I1", "I2", "I6", "I7"]
  log: { timestamp: string, message: string }[];
}
```

### 4. Run Scenario Simulator
`POST /api/scenario/run`
**Request**: `{ config: ScenarioConfig }`
**Response**: `{ impact: Intersection[], optimized: Intersection[] }`
Returns the impact of a scenario (e.g. accident, extreme traffic) on the network and the optimized response.

### 5. Get Environment Timeseries
`GET /api/environment/timeseries`
Returns historical data points for CO2, fuel, waiting time, throughput, etc.
**Response**: `TimeSeriesPoint[]`

### 6. Get Comparison Summary
`GET /api/comparison/summary`
Returns classical vs hybrid optimization comparison metrics.
**Response**: `Metric[]`
