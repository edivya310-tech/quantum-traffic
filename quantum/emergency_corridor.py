"""Emergency Green Corridor Module for Quantum-Enhanced Adaptive Urban Traffic Optimization.

SIMULATED EMERGENCY-PRIORITY MECHANISM:
This module models an emergency vehicle (e.g. Ambulance) requesting a temporary
green corridor along its route through connected urban intersections.

DISCLAIMER / REALISM NOTE:
This is a traffic simulation prototype designed for hackathon demonstration.
It does not directly control real-world physical traffic signals or guarantee
physical emergency vehicle safety.

GRAPH GEOMETRY LIMITATION:
The simplified 2D topological graph (J1-J2-J3-J4) represents connectivity between
intersections but lacks explicit physical 3D compass headings. Directional signal
priorities ("NORTH_SOUTH" vs "EAST_WEST") are assigned using route movement
metadata or explicit directional maps.
"""

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional
import networkx as nx


@dataclass
class EmergencyVehicle:
    """Represents an emergency vehicle requesting a green corridor."""

    vehicle_id: str
    vehicle_type: str
    start_intersection: str
    destination_intersection: str
    priority: str = "HIGH"


def create_road_network() -> nx.Graph:
    """Create and return the NetworkX road network graph of connected intersections."""
    graph = nx.Graph()
    intersections = ["J1", "J2", "J3", "J4"]
    graph.add_nodes_from(intersections)

    # Add physical connections between intersections
    edges = [
        ("J1", "J2"),
        ("J2", "J3"),
        ("J3", "J4"),
        ("J1", "J3"),
        ("J2", "J4"),
    ]
    graph.add_edges_from(edges)
    return graph


def find_emergency_route(
    graph: nx.Graph, start: str, destination: str
) -> List[str]:
    """Find the shortest path route for an emergency vehicle through the road network.

    Args:
        graph: NetworkX graph of connected intersections.
        start: Starting intersection name (e.g., "J1").
        destination: Destination intersection name (e.g., "J4").

    Returns:
        List[str] representing ordered sequence of intersection names along the route.
    """
    if start not in graph:
        raise ValueError(f"Start intersection '{start}' not found in road network.")
    if destination not in graph:
        raise ValueError(
            f"Destination intersection '{destination}' not found in road network."
        )

    return list(nx.shortest_path(graph, source=start, target=destination))


def create_green_corridor(route: List[str]) -> List[str]:
    """Identify intersections requiring emergency priority along the calculated route."""
    return list(route)


def derive_signal_directions(
    route: List[str], custom_directions: Optional[Dict[str, str]] = None
) -> Dict[str, str]:
    """Derive directional signal priorities ("NORTH_SOUTH" or "EAST_WEST") for corridor intersections.

    Args:
        route: List of intersection names in the corridor.
        custom_directions: Optional explicit mapping of intersection -> direction.

    Returns:
        Dict[str, str]: Map of intersection name -> signal priority direction.
    """
    signal_priorities: Dict[str, str] = {}

    default_map = {
        "J1": "EAST_WEST",
        "J2": "EAST_WEST",
        "J3": "NORTH_SOUTH",
        "J4": "NORTH_SOUTH",
    }

    for intersection in route:
        if custom_directions and intersection in custom_directions:
            signal_priorities[intersection] = custom_directions[intersection]
        else:
            signal_priorities[intersection] = default_map.get(
                intersection, "EAST_WEST"
            )

    return signal_priorities


def build_emergency_priority_plan(
    route: List[str], signal_directions: Dict[str, str]
) -> Dict[str, Any]:
    """Build a structured, JSON-serializable emergency priority plan."""
    priority_intersections = create_green_corridor(route)

    return {
        "emergency_active": True,
        "route": list(route),
        "priority_intersections": priority_intersections,
        "signal_priorities": signal_directions,
    }


# Simple global state dictionary for emergency corridor status
_EMERGENCY_STATE: Dict[str, Any] = {
    "emergency_active": False,
    "vehicle": None,
    "plan": None,
}


def activate_emergency(
    vehicle: EmergencyVehicle,
    graph: nx.Graph,
    custom_directions: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Activate the emergency green corridor for a given vehicle."""
    route = find_emergency_route(
        graph, vehicle.start_intersection, vehicle.destination_intersection
    )
    signal_directions = derive_signal_directions(route, custom_directions)
    plan = build_emergency_priority_plan(route, signal_directions)

    global _EMERGENCY_STATE
    _EMERGENCY_STATE = {
        "emergency_active": True,
        "vehicle": asdict(vehicle),
        "plan": plan,
    }
    return dict(_EMERGENCY_STATE)


def deactivate_emergency() -> Dict[str, Any]:
    """Deactivate the emergency corridor and return the system to normal mode."""
    global _EMERGENCY_STATE
    _EMERGENCY_STATE = {
        "emergency_active": False,
        "vehicle": None,
        "plan": None,
    }
    return dict(_EMERGENCY_STATE)


def is_emergency_active() -> bool:
    """Check if an emergency green corridor is currently active."""
    return _EMERGENCY_STATE.get("emergency_active", False)


def get_emergency_state() -> Dict[str, Any]:
    """Get the current emergency state dictionary."""
    return dict(_EMERGENCY_STATE)
