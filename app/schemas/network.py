from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class RoadStatus(str, Enum):
    OPEN = "OPEN"
    CONGESTED = "CONGESTED"
    ACCIDENT = "ACCIDENT"
    CLOSED = "CLOSED"
    BLOCKED = "BLOCKED"

class RoadSchema(BaseModel):
    road_id: str
    source_intersection: str
    destination_intersection: str
    length_meters: float = Field(gt=0)
    lanes: int = 1
    speed_limit_kmh: float = 50.0
    capacity: int = 100
    vehicle_count: int = 0
    queue_length: int = 0
    average_speed: float = 0.0
    congestion_score: float = 0.0
    status: RoadStatus = RoadStatus.OPEN

class IntersectionSchema(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float
    incoming_roads: List[str] = []
    outgoing_roads: List[str] = []
    current_signal_phase: Optional[int] = None
    phase_start_time: Optional[float] = None
    phase_duration: Optional[float] = None
    vehicle_count: int = 0
    queue_length: int = 0
    pedestrian_demand: int = 0
    emergency_priority_status: str = "NONE"

class NetworkSchema(BaseModel):
    id: str
    name: str
    intersections: List[IntersectionSchema] = []
    roads: List[RoadSchema] = []
