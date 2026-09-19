from fastapi import APIRouter
from app.simulation.simulator import simulator_engine
from pydantic import BaseModel

router = APIRouter()

class AddVehicleRequest(BaseModel):
    start_node: str
    end_node: str

@router.get("/state")
def get_simulation_state():
    """Returns the current state of the simulation including all vehicles and signals."""
    vehicles = [
        {
            "id": v.id,
            "start": v.start_node,
            "end": v.end_node,
            "current_edge": f"{v.route[v.current_edge_index]}-{v.route[v.current_edge_index+1]}" if v.current_edge_index < len(v.route) -1 else "done",
            "progress": v.progress,
            "status": v.status,
            "waiting_time": v.waiting_time
        }
        for v in simulator_engine.vehicles.values()
    ]
    
    signals = {
        node_id: {
            "current_green_edge": sig.current_green_edge,
            "time_since_change": sig.time_since_last_change
        }
        for node_id, sig in simulator_engine.signals.items()
    }
    
    # Calculate average wait time and active queues
    active_vehicles = len(vehicles)
    avg_wait = simulator_engine.total_wait_time / active_vehicles if active_vehicles > 0 else 0
    waiting_vehicles = sum(1 for v in simulator_engine.vehicles.values() if v.status == "waiting")

    return {
        "running": simulator_engine.running,
        "time": simulator_engine.current_time,
        "vehicles": vehicles,
        "signals": signals,
        "metrics": {
            "vehicle_count": active_vehicles,
            "waiting_vehicles": waiting_vehicles,
            "avg_wait_time": round(avg_wait, 2),
            "total_throughput": simulator_engine.throughput,
            "optimization_mode": simulator_engine.optimizer.mode
        }
    }

@router.post("/start")
def start_simulation():
    simulator_engine.start()
    return {"status": "started"}

@router.post("/stop")
def stop_simulation():
    simulator_engine.stop()
    return {"status": "stopped"}

@router.post("/tick")
def tick_simulation():
    # Force a tick (useful for frontend-driven clock or manual stepping)
    was_running = simulator_engine.running
    simulator_engine.running = True
    simulator_engine.tick()
    simulator_engine.running = was_running
    return {"status": "ticked", "time": simulator_engine.current_time}

@router.post("/add_vehicle")
def add_vehicle(req: AddVehicleRequest):
    v = simulator_engine.add_vehicle(req.start_node, req.end_node)
    if v:
        return {"status": "success", "vehicle_id": v.id}
    return {"status": "error", "message": "Could not route vehicle"}

class ModeRequest(BaseModel):
    mode: str

@router.post("/mode")
def set_optimization_mode(req: ModeRequest):
    if req.mode in ["fixed", "rule_based", "hybrid_quantum"]:
        simulator_engine.optimizer.mode = req.mode
        return {"status": "success", "mode": req.mode}
    return {"status": "error", "message": "Invalid mode"}
