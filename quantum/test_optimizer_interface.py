"""Test suite for Unified Traffic Optimization Interface."""

import sys
import numpy as np

# Ensure stdout handles UTF-8 encoding on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from quantum.traffic_model import create_sample_traffic
    from quantum.optimizer import optimize_traffic
except ModuleNotFoundError:
    from traffic_model import create_sample_traffic
    from optimizer import optimize_traffic


def main() -> None:
    # 1. Load sample traffic
    intersections = create_sample_traffic()

    # 2. Run Classical optimization via unified interface
    classical_res = optimize_traffic(intersections, method="classical")

    # 3. Run QAOA optimization via unified interface
    qaoa_res = optimize_traffic(intersections, method="qaoa")

    # 4. Print formatted test results
    print("=" * 50)
    print("UNIFIED OPTIMIZER TEST")
    print("=" * 50)
    print()

    print("CLASSICAL RESULT")
    print(f"Method: {classical_res['method']}")
    print(f"Configuration: {classical_res['configuration']}")
    print(f"Cost: {classical_res['cost']}")
    print(f"Intersections: {classical_res['num_intersections']}")
    print()

    print("QAOA RESULT")
    print(f"Method: {qaoa_res['method']}")
    print(f"Configuration: {qaoa_res['configuration']}")
    print(f"Cost: {qaoa_res['cost']}")
    print(f"Intersections: {qaoa_res['num_intersections']}")
    print(f"Optimal Gamma: {qaoa_res['gamma']:.4f}")
    print(f"Optimal Beta: {qaoa_res['beta']:.4f}")
    print(f"Shots: {qaoa_res['shots']}")
    print()

    # 5. Check if QAOA matched classical optimum
    matched = (
        classical_res["configuration"] == qaoa_res["configuration"]
    ) and np.isclose(classical_res["cost"], qaoa_res["cost"])
    match_str = "YES" if matched else "NO"

    print("=" * 50)
    print("COMPARISON SUMMARY")
    print("=" * 50)
    print(f"{'Method':<12} {'Configuration':<20} {'Cost':<10}")
    print("-" * 46)
    print(
        f"{'Classical':<12} {str(classical_res['configuration']):<20} {classical_res['cost']:<10.1f}"
    )
    print(
        f"{'QAOA':<12} {str(qaoa_res['configuration']):<20} {qaoa_res['cost']:<10.1f}"
    )
    print("-" * 46)

    cost_diff = qaoa_res["cost"] - classical_res["cost"]
    print(f"Cost difference (QAOA - Classical): {cost_diff:+.1f}")
    print(f"QAOA matched classical optimum: {match_str}")
    print("=" * 50)
    print()

    # ==================================================
    # VALIDATION / ASSERTIONS
    # ==================================================

    print("=" * 50)
    print("VALIDATION")
    print("=" * 50)

    for res in [classical_res, qaoa_res]:
        m = res["method"]
        # Required keys present
        for key in ["method", "configuration", "cost", "num_intersections"]:
            assert key in res, f"Missing required key '{key}' in {m} result"

        # Configuration length == 4
        assert (
            len(res["configuration"]) == 4
        ), f"Configuration length != 4 in {m} result"

        # Binary values 0 or 1
        assert all(
            val in (0, 1) for val in res["configuration"]
        ), f"Invalid non-binary value in {m} configuration"

        # Num intersections == 4
        assert (
            res["num_intersections"] == 4
        ), f"num_intersections != 4 in {m} result"

        # Cost is numeric
        assert isinstance(
            res["cost"], (int, float)
        ), f"Cost is not numeric in {m} result"

    print("Standard result structure for classical & QAOA: PASS")

    # Input validation test: invalid method
    try:
        optimize_traffic(intersections, method="invalid_method")
        assert False, "Should have raised ValueError for invalid method"
    except ValueError as e:
        assert "method must be 'classical' or 'qaoa'" in str(e)
        print("Validation for invalid method name: PASS")

    # Input validation test: empty intersections
    try:
        optimize_traffic([])
        assert False, "Should have raised ValueError for empty intersections"
    except ValueError as e:
        assert "intersections list cannot be empty" in str(e)
        print("Validation for empty intersections: PASS")

    # Input validation test: wrong intersection count
    try:
        optimize_traffic(intersections[:2])
        assert False, "Should have raised ValueError for wrong intersection count"
    except ValueError as e:
        assert "prototype currently requires exactly 4 intersections" in str(e)
        print("Validation for non-4 intersection count: PASS")

    print()
    print("All interface test assertions passed successfully.")
    print("=" * 50)


if __name__ == "__main__":
    main()
