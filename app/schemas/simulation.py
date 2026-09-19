from enum import Enum
from pydantic import BaseModel
from typing import Optional

class VehicleType(str, Enum):
    CAR = "CAR"
    BUS = "BUS"
    TRUCK = "TRUCK"
    MOTORCYCLE = "MOTORCYCLE"
    AMBULANCE = "AMBULANCE"
    FIRE_TRUCK = "FIRE_TRUCK"
    POLICE = "POLICE"

class EmergencyPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class VehicleSchema(BaseModel):
    vehicle_id: str
    vehicle_type: VehicleType
    current_road: Optional[str] = None
    origin: str
    destination: str
    position: float = 0.0
    speed: float = 0.0
    maximum_speed: float = 50.0
    waiting_time: float = 0.0
    travel_time: float = 0.0
    fuel_consumption: float = 0.0
    co2_emission: float = 0.0
    is_emergency: bool = False
    emergency_type: Optional[str] = None
    priority: Optional[EmergencyPriority] = None
    created_at: float = 0.0
    completed_at: Optional[float] = None
