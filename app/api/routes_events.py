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