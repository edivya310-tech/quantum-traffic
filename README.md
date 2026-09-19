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
