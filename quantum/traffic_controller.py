"""Traffic Controller Orchestration Layer for Quantum-Enhanced Urban Traffic Optimization.

This module unifies dynamic traffic data ingestion, classical/QAOA quantum optimization,
and emergency green corridor override management into a single clean Python interface.
"""

import json
from typing import Any, Dict, List, Optional

try:
    from quantum.traffic_model import TrafficIntersection, create_traffic_from_dicts
    from quantum.optimizer import optimize_traffic
    from quantum.emergency_corridor import (
        EmergencyVehicle,
        activate_emergency,
        create_road_network,
        deactivate_emergency,
    )
except ModuleNotFoundError:
    from traffic_model import TrafficIntersection, create_traffic_from_dicts
    from optimizer import optimize_traffic
    from emergency_corridor import (
        EmergencyVehicle,
        activate_emergency,
        create_road_network,
        deactivate_emergency,
    )


def _sanitize_for_json(obj: Any) -> Any:
    """Helper to convert NumPy types and complex objects into JSON-serializable Python built-ins."""
    if isinstance(obj, dict):
        return {str(k): _sanitize_for_json(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [_sanitize_for_json(v) for v in obj]
    elif isinstance(obj, (int, float, str, bool)):
        return obj
    elif hasattr(obj, "item"):  # NumPy numeric scalars
        return obj.item()
    else:
        return str(obj)


class TrafficController:
    """Single orchestration controller for traffic signal optimization and emergency corridors."""

    def __init__(self, method: str = "qaoa", p: int = 1, shots: int = 1024) -> None:
        """Initialize TrafficController.

        Args:
            method: Optimization method - "qaoa" (default) or "classical".
            p: QAOA circuit depth / layers.
            shots: Simulator measurement shots for QAOA.
        """
        method_clean = method.lower().strip()
        if method_clean not in ("qaoa", "classical"):
            raise ValueError("method must be 'classical' or 'qaoa'")

        self.method: str = method_clean
        self.p: int = p
        self.shots: int = shots

        self.traffic_data: Optional[List[Dict[str, Any]]] = None
        self.intersections: Optional[List[TrafficIntersection]] = None

        self.road_network = create_road_network()
        self.emergency_active: bool = False
        self.emergency_vehicle: Optional[EmergencyVehicle] = None
        self.emergency_plan: Optional[Dict[str, Any]] = None

    def update_traffic(self, traffic_data: List[Dict[str, Any]]) -> None:
        """Update traffic network with new dynamic traffic data.

        Args:
            traffic_data: List of 4 intersection traffic count dictionaries.
        """
        parsed = create_traffic_from_dicts(traffic_data)
        self.traffic_data = traffic_data
        self.intersections = parsed

    def activate_emergency(self, emergency_data: Dict[str, Any]) -> Dict[str, Any]:
        """Activate emergency green corridor for an emergency vehicle.

        Args:
            emergency_data: Dict containing vehicle_id, vehicle_type, start_intersection, destination_intersection.

        Returns:
            Dict[str, Any]: Activated emergency state plan.
        """
        if not isinstance(emergency_data, dict):
            raise ValueError("emergency_data must be a dictionary.")

        req_keys = {
            "vehicle_id",
            "vehicle_type",
            "start_intersection",
            "destination_intersection",
        }
        missing = req_keys - set(emergency_data.keys())
        if missing:
            raise ValueError(f"emergency_data missing required fields: {missing}")

        vehicle = EmergencyVehicle(
            vehicle_id=str(emergency_data["vehicle_id"]),
            vehicle_type=str(emergency_data["vehicle_type"]),
            start_intersection=str(emergency_data["start_intersection"]),
            destination_intersection=str(emergency_data["destination_intersection"]),
            priority=str(emergency_data.get("priority", "HIGH")),
        )

        state = activate_emergency(vehicle, self.road_network)
        self.emergency_active = True
        self.emergency_vehicle = vehicle
        self.emergency_plan = state["plan"]

        return self._build_emergency_control_result()

    def deactivate_emergency(self) -> Dict[str, Any]:
        """Deactivate active emergency corridor and return system to normal optimization."""
        deactivate_emergency()
        self.emergency_active = False
        self.emergency_vehicle = None
        self.emergency_plan = None

        return {"mode": "normal", "emergency_active": False}

    def compute_control_plan(self) -> Dict[str, Any]:
        """Compute the current unified traffic control decision plan.

        Returns:
            Dict[str, Any]: JSON-serializable decision dictionary for either normal or emergency mode.
        """
        if self.emergency_active and self.emergency_plan and self.emergency_vehicle:
            return self._build_emergency_control_result()

        if self.intersections is None:
            raise ValueError("No traffic data loaded. Call update_traffic() first.")

        # Execute normal optimization
        opt_res = optimize_traffic(
            self.intersections, method=self.method, p=self.p, shots=self.shots
        )

        res = {
            "mode": "normal",
            "method": self.method,
            "configuration": opt_res["configuration"],
            "cost": float(opt_res["cost"]),
            "num_intersections": opt_res["num_intersections"],
        }

        if self.method == "qaoa":
            res["gamma"] = float(opt_res["gamma"])
            res["beta"] = float(opt_res["beta"])
            res["shots"] = int(opt_res["shots"])
            res["counts"] = opt_res["counts"]
        elif "evaluations" in opt_res:
            res["evaluations"] = opt_res["evaluations"]

        return _sanitize_for_json(res)

    def _build_emergency_control_result(self) -> Dict[str, Any]:
        """Format the active emergency control plan output."""
        if not self.emergency_vehicle or not self.emergency_plan:
            raise ValueError("Emergency vehicle or plan not initialized.")

        res = {
            "mode": "emergency",
            "vehicle_id": self.emergency_vehicle.vehicle_id,
            "vehicle_type": self.emergency_vehicle.vehicle_type,
            "start_intersection": self.emergency_vehicle.start_intersection,
            "destination_intersection": self.emergency_vehicle.destination_intersection,
            "route": self.emergency_plan["route"],
            "green_corridor": self.emergency_plan["priority_intersections"],
            "priority_plan": self.emergency_plan["signal_priorities"],
            "num_intersections": len(self.intersections) if self.intersections else 4,
        }
        return _sanitize_for_json(res)

    def get_status(self) -> Dict[str, Any]:
        """Return the current controller status summary."""
        status = {
            "method": self.method,
            "emergency_active": self.emergency_active,
            "traffic_loaded": self.intersections is not None,
            "num_intersections": len(self.intersections) if self.intersections else 0,
        }
        if self.emergency_active and self.emergency_vehicle:
            status["emergency_vehicle_id"] = self.emergency_vehicle.vehicle_id

        return _sanitize_for_json(status)
