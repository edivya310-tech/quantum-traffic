from typing import Dict, List
from app.schemas.simulation import VehicleSchema, VehicleType, EmergencyPriority
import time
import random
import uuid

class VehicleManager:
    def __init__(self, network, config):
        self.network = network
        self.config = config
        self.vehicles: Dict[str, VehicleSchema] = {}
        
    def generate_traffic(self, traffic_level: str, seed: int = None):
        if seed is not None:
            random.seed(seed)
            
        rate_map = {
            "LOW": 5,
            "NORMAL": 15,
            "HIGH": 30,
            "PEAK": 50,
            "CUSTOM": 20
        }
        
        vehicles_per_min = rate_map.get(traffic_level, 15)
        # simplistic generation logic
        if random.random() < (vehicles_per_min / 60.0):
            self.create_random_vehicle()
            
    def create_random_vehicle(self):
        if not self.network or not self.network.intersections:
            return None
            
        # Select random start and end intersections
        start_node = random.choice(self.network.intersections)
        end_node = random.choice([n for n in self.network.intersections if n.id != start_node.id])
        
        vid = f"V-{uuid.uuid4().hex[:6]}"
        vtype = random.choices(
            [VehicleType.CAR, VehicleType.BUS, VehicleType.TRUCK, VehicleType.MOTORCYCLE],
            weights=[0.7, 0.1, 0.1, 0.1]
        )[0]
        
        v = VehicleSchema(
            vehicle_id=vid,
            vehicle_type=vtype,
            origin=start_node.id,
            destination=end_node.id,
            created_at=time.time()
        )
        self.vehicles[vid] = v
        return v
        
    def update_positions(self, dt: float):
        for vid, v in self.vehicles.items():
            if v.completed_at is None:
                # very simplified update logic
                # in a real simulation, we calculate route via NetworkX and move along edges
                v.travel_time += dt
                v.waiting_time += dt * 0.1 # just placeholder
                
                # Fuel estimation placeholder
                v.fuel_consumption += dt * 0.005
                v.co2_emission = v.fuel_consumption * 2.31
                
    def get_metrics(self):
        active = [v for v in self.vehicles.values() if v.completed_at is None]
        completed = [v for v in self.vehicles.values() if v.completed_at is not None]
        
        return {
            "active_vehicles": len(active),
            "completed_vehicles": len(completed),
            "average_waiting_time": sum(v.waiting_time for v in self.vehicles.values()) / max(1, len(self.vehicles)),
            "total_fuel": sum(v.fuel_consumption for v in self.vehicles.values()),
            "total_co2": sum(v.co2_emission for v in self.vehicles.values())
        }
