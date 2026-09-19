from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class EventType(str, Enum):
    CONGESTION = "CONGESTION"
    ACCIDENT = "ACCIDENT"
    ROAD_CLOSURE = "ROAD_CLOSURE"
    EMERGENCY_VEHICLE = "EMERGENCY_VEHICLE"
    PEDESTRIAN_SURGE = "PEDESTRIAN_SURGE"
    CUSTOM = "CUSTOM"

class EventStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RESOLVED = "RESOLVED"

class EventSchema(BaseModel):
    event_id: str
    type: EventType
    location: str # Could be intersection id or road id
    severity: float = 0.5 # 0.0 to 1.0
    start_time: float
    duration_seconds: float
    affected_roads: List[str] = []
    affected_intersections: List[str] = []
    status: EventStatus = EventStatus.ACTIVE
    description: str = ""
