"""Classical Brute-Force Traffic Signal Optimizer for 4-Intersection Network.

This module evaluates all 2^4 = 16 binary signal configurations to establish
a deterministic classical baseline for traffic pressure cost minimization.
"""

import itertools
from typing import Any, Dict, List

try:
    from quantum.traffic_model import TrafficIntersection
except ModuleNotFoundError:
    from traffic_model import TrafficIntersection


def calculate_cost(
    intersections: List[TrafficIntersection], configuration: List[int]
) -> int:
    """Calculate the total traffic pressure waiting cost for a given signal configuration.

    Cost model for each intersection i and decision x_i:
        - If x_i = 0 (East-West priority): North-South traffic waits -> cost_i = NS_pressure_i
        - If x_i = 1 (North-South priority): East-West traffic waits -> cost_i = EW_pressure_i

    Args:
        intersections: List of TrafficIntersection objects.
        configuration: List of 4 binary values (0 or 1) representing signal decisions.

    Returns:
        Total integer traffic pressure cost across all intersections.
    """
    if len(intersections) != len(configuration):
        raise ValueError("Number of intersections must match configuration length.")

    total_cost = 0
    for intersection, decision in zip(intersections, configuration):
        if decision == 0:
            # EW priority -> NS traffic experiences waiting pressure
            total_cost += intersection.north_south_pressure
        elif decision == 1:
            # NS priority -> EW traffic experiences waiting pressure
            total_cost += intersection.east_west_pressure
        else:
            raise ValueError(f"Invalid decision value: {decision}. Must be 0 or 1.")

    return total_cost


def optimize_traffic(intersections: List[TrafficIntersection]) -> Dict[str, Any]:
    """Perform brute-force evaluation over all 16 binary signal configurations.

    Args:
        intersections: List of 4 TrafficIntersection objects.

    Returns:
        Dictionary containing:
        - "best_configuration": List[int] of 4 binary signal decisions
        - "best_cost": int minimum cost found
        - "evaluations": List of dicts, each with "configuration" and "cost"
    """
    num_intersections = len(intersections)
    evaluations: List[Dict[str, Any]] = []

    best_config: List[int] = []
    best_cost: float = float("inf")

    # Generate all 2^num_intersections binary configurations (from [0,0,0,0] to [1,1,1,1])
    for config_tuple in itertools.product([0, 1], repeat=num_intersections):
        config = list(config_tuple)
        cost = calculate_cost(intersections, config)

        evaluations.append({"configuration": config, "cost": cost})

        if cost < best_cost:
            best_cost = cost
            best_config = config

    return {
        "best_configuration": best_config,
        "best_cost": int(best_cost),
        "evaluations": evaluations,
    }
