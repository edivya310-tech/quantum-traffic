from pydantic import BaseModel
from typing import Dict, Any, Optional

class ComparisonResultSchema(BaseModel):
    average_waiting_time: float
    maximum_queue: int
    throughput: int
    fuel_consumption: float
    co2_emission: float
    emergency_travel_time: Optional[float] = None
    emergency_delay: Optional[float] = None
    runtime: float

class ComparisonResponseSchema(BaseModel):
    fixed_time: ComparisonResultSchema
    rule_based: ComparisonResultSchema
    hybrid_quantum: ComparisonResultSchema
