# Q-TRAFFIC: Quantum-Enhanced Adaptive Urban Traffic Optimization

A smart-city command center that shows, in real time and in plain language, *why* a hybrid quantum-classical optimizer is making the traffic network faster, cleaner, and safer than a classical baseline.

## Quick Start

```bash
npm install
npm run dev
```
Navigate to `http://localhost:5173` to view the frontend.

## Stack Summary

- **Frontend Framework**: React + Vite
- **Styling**: Tailwind CSS v4 (with custom CSS variables for tokenized theming)
- **Icons**: lucide-react
- **Charting**: Recharts
- **Routing**: react-router-dom

## Folder Structure

```
src/
  components/   → Dumb, reusable, presentational components (e.g., MetricCard, TrafficNetwork)
  pages/        → One file per sidebar route, composed from components
  context/      → Global state (TrafficContext - manages intersections and mock API integration)
  data/         → Pure mock data definitions
  hooks/        → Shared React hooks
  utils/        → api.js (fetch layer), metrics.js (pure math), format.js
```

## Backend Contract

The application is structured to easily integrate with a real Python/FastAPI + Qiskit backend. Currently, `src/utils/api.js` returns mock data. To integrate the real backend, replace the mock implementations in `api.js` with real `fetch` calls to these endpoints:

- `GET  /api/network/state` → `Intersection[]`
- `POST /api/optimize/run {state}` → `{ id, before, after, delta }[]`
- `POST /api/emergency/activate {o,d}` → `{ route: string[], log: Event[] }`
- `POST /api/scenario/run {config}` → `{ impact, optimized }`
- `GET  /api/environment/timeseries` → `TimeSeriesPoint[]`
- `GET  /api/comparison/summary` → `Metric[]`

For exact typescript shapes, please view `docs/API_CONTRACT.md`.

## What's real vs. simulated

The frontend interface, state management, routing, and metric derivations (such as the health score and derived environmental impacts from queue lengths) are fully functional production-ready React code. However, the **underlying data generation is simulated**. The QUBO formulation, QAOA quantum optimization steps, and scenario impacts are currently mocked via client-side logic and timers in `api.js`. In a production environment, this dashboard would ingest real historical SCATS data as the classical baseline, and run a calibrated SUMO micro-simulation powered by IBM Qiskit backend services to generate the hybrid results.
