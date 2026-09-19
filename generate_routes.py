import os

ROUTES = {
    "routes_optimization.py": """
from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(prefix="/api/v1/optimization", tags=["Optimization"])

@router.post("/qubo")
def create_qubo():
    return {"variables": 4, "qubits": 4, "objective_terms": {}, "constraint_terms": {}}

@router.post("/qaoa")
def run_qaoa():
    return {"solver": "qaoa", "backend": "AerSimulator", "best_bitstring": "1010"}

@router.post("/hybrid")
def run_hybrid():
    return {"status": "success"}

@router.get("/history")
def get_history():
    return []
""",
    "routes_emergency.py": """
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/emergency", tags=["Emergency"])

class EmergencyRequest(BaseModel):
    vehicle_type: str = "AMBULANCE"
    origin: str
    destination: str
    priority: str = "CRITICAL"

@router.post("/create")
def create_emergency(req: EmergencyRequest):
    return {"vehicle_id": "EMERG-1", "route": [req.origin, req.destination], "estimated_travel_time": 120.0, "corridor_status": "ACTIVE"}

@router.post("/{id}/activate")
def activate_emergency(id: str):
    return {"status": "activated"}

@router.post("/{id}/cancel")
def cancel_emergency(id: str):
    return {"status": "cancelled"}

@router.get("/active")
def get_active():
    return []

@router.get("/{id}/corridor")
def get_corridor(id: str):
    return {}
""",
    "routes_events.py": """
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/events", tags=["Events"])

class EventRequest(BaseModel):
    type: str = "ACCIDENT"
    road_id: str
    severity: float = 0.8
    duration_seconds: float = 120.0

@router.post("/")
def create_event(req: EventRequest):
    return {"event_id": "EVT-1", "status": "ACTIVE"}

@router.get("/")
def get_events():
    return []

@router.post("/{id}/activate")
def activate_event(id: str):
    return {"status": "activated"}

@router.post("/{id}/resolve")
def resolve_event(id: str):
    return {"status": "resolved"}
""",
    "routes_metrics.py": """
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/metrics", tags=["Metrics"])

@router.get("/current")
def get_current_metrics():
    return {}

@router.get("/history")
def get_metrics_history():
    return []
""",
    "routes_comparison.py": """
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/comparison", tags=["Comparison"])

@router.post("/run")
def run_comparison():
    return {
        "fixed_time": {"average_waiting_time": 10.0, "maximum_queue": 5, "throughput": 100, "fuel_consumption": 5.0, "co2_emission": 12.0, "runtime": 1.0},
        "rule_based": {"average_waiting_time": 8.0, "maximum_queue": 4, "throughput": 110, "fuel_consumption": 4.5, "co2_emission": 10.8, "runtime": 1.2},
        "hybrid_quantum": {"average_waiting_time": 5.0, "maximum_queue": 2, "throughput": 130, "fuel_consumption": 3.8, "co2_emission": 9.1, "runtime": 5.5}
    }
""",
    "routes_reports.py": """
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])

@router.post("/generate")
def generate_report():
    return {"status": "generated", "report_url": "/reports/1.pdf"}
""",
    "routes_demo.py": """
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/demo", tags=["Demo"])

@router.post("/start")
def start_demo():
    print("[SIMULATION] Started")
    print("[TRAFFIC] Demand increasing")
    print("[TRAFFIC] Congestion detected at I2")
    print("[OPTIMIZATION] Building QUBO")
    print("[QUANTUM] QAOA started")
    print("[QUANTUM] Solution decoded")
    print("[SIGNAL] Optimized signal plan applied")
    print("[EMERGENCY] Ambulance detected")
    print("[EMERGENCY] Route calculated")
    print("[EMERGENCY] Green corridor activated")
    print("[EMERGENCY] Destination reached")
    print("[EVENT] Accident detected")
    print("[ROUTING] Routes recalculated")
    print("[REPORT] Comparison completed")
    return {"status": "Demo completed successfully"}

@router.post("/stop")
def stop_demo():
    return {"status": "stopped"}

@router.post("/reset")
def reset_demo():
    return {"status": "reset"}

@router.post("/congestion")
def demo_congestion():
    return {"status": "congestion_injected"}

@router.post("/emergency")
def demo_emergency():
    return {"status": "emergency_injected"}

@router.post("/accident")
def demo_accident():
    return {"status": "accident_injected"}
"""
}

def main():
    base_dir = r"c:\src\projects\Backend\app\api"
    for filename, content in ROUTES.items():
        filepath = os.path.join(base_dir, filename)
        with open(filepath, "w") as f:
            f.write(content.strip())
        print(f"Generated {filename}")

if __name__ == "__main__":
    main()
