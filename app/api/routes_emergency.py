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