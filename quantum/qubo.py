"""QUBO Formulation for Quantum-Enhanced Adaptive Urban Traffic Optimization.

MATHEMATICAL CONVENTION AND FORMULATION:
We express the traffic pressure cost minimization problem in QUBO form:

    E(x) = x^T Q x + offset

where:
    x = [x_1, x_2, x_3, x_4]^T  is a vector of binary variables in {0, 1}^4.
    x_i = 0 represents East-West priority at intersection i (NS traffic waits).
    x_i = 1 represents North-South priority at intersection i (EW traffic waits).

Algebraic Derivation:
    cost_i(x_i) = NS_i * (1 - x_i) + EW_i * x_i
                = NS_i + (EW_i - NS_i) * x_i

Since intersections are independent in this model, there are no x_i * x_j interaction terms.
Thus, Q is a 4x4 diagonal matrix where:
    Q_ii = EW_i - NS_i

Since x_i^2 = x_i for binary variables x_i in {0, 1}:
    x^T Q x = sum_i Q_ii * x_i^2 = sum_i (EW_i - NS_i) * x_i

The constant offset is:
    offset = sum_i NS_i

Therefore:
    E(x) = x^T Q x + offset = sum_i NS_i + sum_i (EW_i - NS_i) * x_i = Total Classical Cost C(x)
"""

import itertools
from typing import Any, Dict, List, Tuple
import numpy as np

try:
    from quantum.traffic_model import TrafficIntersection
except ModuleNotFoundError:
    from traffic_model import TrafficIntersection


def build_qubo(intersections: List[TrafficIntersection]) -> Tuple[np.ndarray, float]:
    """Construct the QUBO matrix Q and constant offset from traffic intersections.

    Args:
        intersections: List of TrafficIntersection objects.

    Returns:
        Tuple of (Q, offset):
            Q: 4x4 numpy float array representing the QUBO matrix.
            offset: float representing constant cost offset sum_i (NS_i).
    """
    n = len(intersections)
    Q = np.zeros((n, n), dtype=float)
    offset = 0.0

    for i, intersection in enumerate(intersections):
        ns = float(intersection.north_south_pressure)
        ew = float(intersection.east_west_pressure)

        # Diagonal coefficient Q_ii = EW_i - NS_i
        Q[i, i] = ew - ns

        # Constant offset accumulates NS_i
        offset += ns

    return Q, offset


def evaluate_qubo(
    Q: np.ndarray, configuration: List[int], offset: float = 0.0
) -> float:
    """Evaluate the QUBO energy E(x) = x^T Q x + offset for a binary configuration vector.

    Args:
        Q: NxN QUBO numpy matrix.
        configuration: List of binary values (0 or 1) of length N.
        offset: Constant float offset added to x^T Q x.

    Returns:
        Total QUBO cost (float).
    """
    x = np.array(configuration, dtype=float)
    raw_energy = float(x.T @ Q @ x)
    return raw_energy + offset


def solve_qubo_bruteforce(
    Q: np.ndarray, offset: float = 0.0
) -> Dict[str, Any]:
    """Brute-force evaluate all binary configurations against the QUBO model.

    This function evaluates all 2^N configurations using evaluate_qubo.
    It is used strictly for validating the QUBO against classical results.

    Args:
        Q: NxN QUBO matrix.
        offset: Constant float offset.

    Returns:
        Dictionary with keys:
        - "best_configuration": List[int]
        - "best_cost": float
        - "evaluations": List of dicts with "configuration", "raw_energy", and "cost"
    """
    n = Q.shape[0]
    evaluations: List[Dict[str, Any]] = []

    best_config: List[int] = []
    best_cost: float = float("inf")

    for config_tuple in itertools.product([0, 1], repeat=n):
        config = list(config_tuple)
        x = np.array(config, dtype=float)
        raw_energy = float(x.T @ Q @ x)
        total_cost = raw_energy + offset

        evaluations.append(
            {
                "configuration": config,
                "raw_energy": raw_energy,
                "cost": total_cost,
            }
        )

        if total_cost < best_cost:
            best_cost = total_cost
            best_config = config

    return {
        "best_configuration": best_config,
        "best_cost": best_cost,
        "evaluations": evaluations,
    }
