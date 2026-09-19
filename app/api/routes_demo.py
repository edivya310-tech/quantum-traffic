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