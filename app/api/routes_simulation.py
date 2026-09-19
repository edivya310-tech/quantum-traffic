from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/v1/simulation", tags=["Simulation"])

class StartSimulationRequest(BaseModel):
    scenario: str = "NORMAL_TRAFFIC"
    duration_seconds: int = 600
    traffic_level: str = "HIGH"
    random_seed: Optional[int] = 42
    solver: str = "hybrid_quantum"

@router.post("/start")
def start_simulation(request: StartSimulationRequest, background_tasks: BackgroundTasks):
    # Start the simulation background process
    return {"message": "Simulation started", "status": "running"}

@router.post("/stop")
def stop_simulation():
    return {"message": "Simulation stopped"}

@router.post("/pause")
def pause_simulation():
    return {"message": "Simulation paused"}

@router.post("/resume")
def resume_simulation():
    return {"message": "Simulation resumed"}

@router.post("/reset")
def reset_simulation():
    return {"message": "Simulation reset"}

@router.get("/status")
def get_status():
    return {"status": "STOPPED", "time": 0.0}

@router.get("/state")
def get_state():
    return {"network": {}, "vehicles": [], "events": []}
