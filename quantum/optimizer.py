"""Unified Optimization Interface for Quantum-Enhanced Adaptive Urban Traffic Optimization.

This module provides a single entry point `optimize_traffic` (and `optimize_traffic_from_dicts`)
for executing traffic signal optimization using either classical brute-force evaluation or QAOA quantum algorithm.

Signal Decision Mapping:
    configuration[0] -> J1 (x1)
    configuration[1] -> J2 (x2)
    configuration[2] -> J3 (x3)
    configuration[3] -> J4 (x4)

    0 = East-West green light priority (North-South traffic waits)
    1 = North-South green light priority (East-West traffic waits)
"""

from typing import Any, Dict, List

try:
    from quantum.traffic_model import TrafficIntersection, create_traffic_from_dicts
    from quantum.classical_optimizer import optimize_traffic as run_classical_optimizer
    from quantum.qaoa import run_qaoa
except ModuleNotFoundError:
    from traffic_model import TrafficIntersection, create_traffic_from_dicts
    from classical_optimizer import optimize_traffic as run_classical_optimizer
    from qaoa import run_qaoa


def optimize_traffic(
    intersections: List[TrafficIntersection],
    method: str = "qaoa",
    p: int = 1,
    shots: int = 1024,
) -> Dict[str, Any]:
    """Optimize traffic signal decisions across intersections using requested algorithm method.

    Args:
        intersections: List of TrafficIntersection objects (expects exactly 4 for prototype).
        method: Optimization algorithm to use - "qaoa" (default) or "classical".
        p: QAOA circuit depth / layers (used when method="qaoa").
        shots: Number of measurement shots for simulator (used when method="qaoa").

    Returns:
        Standardized dictionary containing optimization results:
        - "method": str ("classical" or "qaoa")
        - "configuration": List[int] binary decisions [x1, x2, x3, x4]
        - "cost": float total waiting pressure cost
        - "num_intersections": int count of intersections
        - "gamma", "beta", "shots", "counts" (present when method="qaoa")
        - "evaluations" (present when method="classical")

    Raises:
        ValueError: If input validation fails or invalid method is requested.
    """
    # 1. Input Validation
    if not intersections:
        raise ValueError("intersections list cannot be empty.")

    if len(intersections) != 4:
        raise ValueError(
            f"Traffic optimization prototype currently requires exactly 4 intersections, got {len(intersections)}."
        )

    for intersection in intersections:
        if (
            intersection.north < 0
            or intersection.south < 0
            or intersection.east < 0
            or intersection.west < 0
        ):
            raise ValueError(
                f"Intersection {intersection.name} contains invalid negative traffic counts."
            )

    method_normalized = method.lower().strip()
    if method_normalized not in ("classical", "qaoa"):
        raise ValueError("method must be 'classical' or 'qaoa'")

    # 2. Method Execution
    if method_normalized == "classical":
        classical_res = run_classical_optimizer(intersections)
        return {
            "method": "classical",
            "configuration": classical_res["best_configuration"],
            "cost": float(classical_res["best_cost"]),
            "num_intersections": len(intersections),
            "evaluations": classical_res["evaluations"],
        }

    elif method_normalized == "qaoa":
        qaoa_res = run_qaoa(intersections, p=p, shots=shots)
        return {
            "method": "qaoa",
            "configuration": qaoa_res["configuration"],
            "cost": float(qaoa_res["cost"]),
            "num_intersections": len(intersections),
            "gamma": qaoa_res["gamma"],
            "beta": qaoa_res["beta"],
            "shots": qaoa_res["shots"],
            "counts": qaoa_res["counts"],
        }

    raise ValueError("method must be 'classical' or 'qaoa'")


def optimize_traffic_from_dicts(
    data: List[Dict[str, Any]],
    method: str = "qaoa",
    p: int = 1,
    shots: int = 1024,
) -> Dict[str, Any]:
    """Convenience function to parse traffic dictionary data and optimize signal decisions.

    Args:
        data: List of 4 traffic dictionaries (each containing name, north, south, east, west).
        method: "qaoa" (default) or "classical".
        p: QAOA depth (layers).
        shots: Number of measurement shots.

    Returns:
        Standardized optimization result dictionary.
    """
    intersections = create_traffic_from_dicts(data)
    return optimize_traffic(intersections, method=method, p=p, shots=shots)
