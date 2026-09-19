from pydantic import BaseModel
from typing import List, Optional

class SignalPhase(BaseModel):
    phase_id: int
    green_roads: List[str]
    red_roads: List[str]

class SignalSchema(BaseModel):
    intersection_id: str
    phases: List[SignalPhase]
    current_phase_index: int = 0
    phase_timer: float = 0.0
    
    green_duration: float = 30.0
    yellow_duration: float = 3.0
    all_red_duration: float = 1.0
    
    is_yellow: bool = False
    is_all_red: bool = False
