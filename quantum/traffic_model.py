"""Traffic Model for Quantum-Enhanced Adaptive Urban Traffic Optimization.

MATHEMATICAL ASSUMPTION:
This is a simplified hackathon traffic-pressure model.
We are approximating the pressure/waiting demand for each signal direction
using the number of vehicles waiting on that direction.
This is NOT a full microscopic traffic simulation.
The purpose is to create a small optimization problem that can later be
converted into a QUBO (Quadratic Unconstrained Binary Optimization) problem
and solved using QAOA (Quantum Approximate Optimization Algorithm).
"""

from dataclasses import dataclass
from typing import Any, Dict, List



@dataclass
class TrafficIntersection:
    """Represents an urban traffic intersection with vehicle counts from four directions.

    Signal Decision Mapping (documented for upcoming optimization steps):
        Binary optimization variable x_i for intersection i:
            0 = East-West (EW) green light priority
            1 = North-South (NS) green light priority
    """

    name: str
    north: int
    south: int
    east: int
    west: int

    @property
    def total_traffic(self) -> int:
        """Calculate the total traffic volume passing through the intersection."""
        return self.north + self.south + self.east + self.west

    @property
    def north_south_pressure(self) -> int:
        """Calculate the traffic pressure on the North-South axis."""
        return self.north + self.south

    @property
    def east_west_pressure(self) -> int:
        """Calculate the traffic pressure on the East-West axis."""
        return self.east + self.west


def create_sample_traffic() -> List[TrafficIntersection]:
    """Create and return sample traffic data for four connected urban intersections (J1, J2, J3, J4)."""
    j1 = TrafficIntersection(name="J1", north=20, south=15, east=35, west=30)
    j2 = TrafficIntersection(name="J2", north=40, south=25, east=15, west=20)
    j3 = TrafficIntersection(name="J3", north=10, south=20, east=45, west=40)
    j4 = TrafficIntersection(name="J4", north=30, south=35, east=25, west=15)

    return [j1, j2, j3, j4]


def create_traffic_from_dicts(data: List[Dict[str, Any]]) -> List[TrafficIntersection]:
    """Convert a list of traffic dictionary objects into TrafficIntersection instances with validation.

    Args:
        data: List of dictionaries containing intersection traffic counts.

    Returns:
        List[TrafficIntersection] preserving the input order.

    Raises:
        ValueError: If data structure or values violate validation constraints.
    """
    if not isinstance(data, list):
        raise ValueError("Traffic data must be provided as a list.")

    if len(data) != 4:
        raise ValueError("Exactly 4 intersections are required.")

    required_keys = {"name", "north", "south", "east", "west"}
    names_seen = set()
    intersections: List[TrafficIntersection] = []

    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Intersection item at index {idx} must be a dictionary.")

        missing = required_keys - set(item.keys())
        if missing:
            raise ValueError(
                f"Intersection at index {idx} missing required fields: {missing}"
            )

        name = str(item["name"]).strip()
        if not name:
            raise ValueError(f"Intersection at index {idx} has invalid empty name.")

        if name in names_seen:
            raise ValueError("Duplicate intersection name.")
        names_seen.add(name)

        for direction in ["north", "south", "east", "west"]:
            val = item[direction]
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                raise ValueError(
                    f"Traffic value for '{direction}' at {name} must be numeric."
                )
            if val < 0:
                raise ValueError("Traffic values cannot be negative.")

        intersections.append(
            TrafficIntersection(
                name=name,
                north=int(item["north"]),
                south=int(item["south"]),
                east=int(item["east"]),
                west=int(item["west"]),
            )
        )

    return intersections



def main() -> None:
    """Display the traffic network details for all sample intersections."""
    intersections = create_sample_traffic()

    print("Traffic Network\n")
    for intersection in intersections:
        print(f"{intersection.name}:")
        print(f"  North: {intersection.north}")
        print(f"  South: {intersection.south}")
        print(f"  East: {intersection.east}")
        print(f"  West: {intersection.west}")
        print(f"  Total: {intersection.total_traffic}")
        print(f"  NS Pressure: {intersection.north_south_pressure}")
        print(f"  EW Pressure: {intersection.east_west_pressure}")
        print()


if __name__ == "__main__":
    main()
