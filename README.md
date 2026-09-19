<<<<<<< HEAD
# Quantum-Enhanced Adaptive Urban Traffic Optimization Platform

This is the backend system for the Quantum-Enhanced Adaptive Urban Traffic Optimization Platform, demonstrating hybrid quantum-classical optimization for urban traffic signal control.

## Features
- **Traffic Simulation**: A custom discrete-time simulation engine managing vehicles, intersections, and signals.
- **Quantum Optimization**: Uses Qiskit to formulate the signal control problem as a QUBO and solves it via QAOA using `AerSimulator`.
- **Emergency Priority**: Detects emergency vehicles (e.g. ambulances) and establishes green corridors.
- **Event Handling**: Dynamically manages accidents, congestion, and road closures.
- **Classical Baselines**: Includes fixed-time and rule-based adaptive algorithms for comparison against quantum optimization.
- **REST APIs**: FastAPI backend with comprehensive endpoints for controlling the simulation and running demonstrations.

## Installation (Windows)

1. Ensure you have Python 3.10+ installed.
2. Create and activate a virtual environment:
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

## Configuration

Copy `.env.example` to `.env` if you wish to change any defaults.

## Running the Backend

Start the FastAPI application:
```cmd
.venv\Scripts\activate
uvicorn app.main:app --reload
```

Then visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access the interactive Swagger UI and test the API endpoints.

## Scientific Disclaimer

This project is a prototype designed to demonstrate how quantum computing (specifically QUBO/QAOA workflows) could theoretically be applied to traffic optimization. The results are based on simulated data. It does not claim guaranteed real-world congestion reduction, fuel savings, or quantum advantage over state-of-the-art classical heuristics on actual hardware.
=======
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
>>>>>>> ea9b587b0895d8c5870800a522ee68670223e942
