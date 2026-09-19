"""Test script and validation suite for QUBO Traffic Optimization formulation."""

import sys
import numpy as np

# Ensure stdout handles UTF-8 encoding on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from quantum.traffic_model import create_sample_traffic
    from quantum.classical_optimizer import calculate_cost, optimize_traffic
    from quantum.qubo import build_qubo, evaluate_qubo, solve_qubo_bruteforce
except ModuleNotFoundError:
    from traffic_model import create_sample_traffic
    from classical_optimizer import calculate_cost, optimize_traffic
    from qubo import build_qubo, evaluate_qubo, solve_qubo_bruteforce


def main() -> None:
    print("=" * 50)
    print("QUBO TRAFFIC OPTIMIZATION")
    print("=" * 50)
    print()

    # 1. Create sample traffic network
    intersections = create_sample_traffic()

    # 2. Build QUBO formulation
    Q, offset = build_qubo(intersections)

    print("QUBO Matrix:")
    print(Q)
    print()
    print("Offset:")
    print(offset)
    print()

    # 3. Evaluate all 16 configurations using QUBO brute-force solver
    qubo_result = solve_qubo_bruteforce(Q, offset)
    classical_result = optimize_traffic(intersections)

    qubo_evals = qubo_result["evaluations"]

    # 4. Print each configuration with QUBO cost and Classical cost
    for item in qubo_evals:
        config = item["configuration"]
        qubo_cost = item["cost"]
        classical_cost = calculate_cost(intersections, config)
        print(f"Configuration {config}")
        print(f"  QUBO Cost: {qubo_cost}")
        print(f"  Classical Cost: {classical_cost}")
        print()

    qubo_best_config = qubo_result["best_configuration"]
    qubo_best_cost = qubo_result["best_cost"]

    classical_best_config = classical_result["best_configuration"]
    classical_best_cost = classical_result["best_cost"]

    print(f"QUBO Best Configuration: {qubo_best_config}")
    print(f"QUBO Best Cost: {qubo_best_cost}")
    print()
    print(f"Classical Best Configuration: {classical_best_config}")
    print(f"Classical Best Cost: {classical_best_cost}")
    print()

    # ==================================================
    # REQUIRED VALIDATION / ASSERTIONS
    # ==================================================

    print("=" * 50)
    print("VALIDATION")
    print("=" * 50)

    # TEST 1: Q must be a 4x4 matrix
    assert Q.shape == (4, 4), f"TEST 1 FAILED: Expected shape (4, 4), got {Q.shape}"
    print("QUBO matrix dimensions: PASS")

    # TEST 2: Q must be a diagonal matrix for this independent-intersection model
    assert np.all(
        Q - np.diag(np.diagonal(Q)) == 0
    ), "TEST 2 FAILED: Q contains non-zero off-diagonal elements"
    print("QUBO diagonal structure: PASS")

    # TEST 3: Calculated offset should equal 195 for sample traffic data
    assert (
        offset == 195.0
    ), f"TEST 3 FAILED: Expected offset 195.0, got {offset}"
    print(f"Calculated offset equal to 195: PASS")

    # TEST 4: Diagonal coefficients should correspond to EW - NS ([30, -30, 55, -25])
    expected_diag = np.array([30.0, -30.0, 55.0, -25.0])
    assert np.array_equal(
        np.diagonal(Q), expected_diag
    ), f"TEST 4 FAILED: Expected diagonal {expected_diag}, got {np.diagonal(Q)}"
    print("Diagonal coefficients match EW - NS: PASS")

    # TEST 5: Exactly 16 binary configurations must be evaluated
    assert (
        len(qubo_evals) == 16
    ), f"TEST 5 FAILED: Expected 16 evaluations, got {len(qubo_evals)}"
    print("All 16 configurations evaluated: PASS")

    # TEST 6: Every configuration must contain exactly four binary values
    for item in qubo_evals:
        config = item["configuration"]
        assert len(config) == 4 and all(
            val in (0, 1) for val in config
        ), f"TEST 6 FAILED: Invalid binary configuration {config}"

    # TEST 7: For EVERY configuration, QUBO cost must equal classical cost
    all_costs_match = True
    for item in qubo_evals:
        config = item["configuration"]
        qubo_c = item["cost"]
        class_c = float(calculate_cost(intersections, config))
        if not np.isclose(qubo_c, class_c):
            all_costs_match = False
            print(
                f"Mismatch for config {config}: QUBO={qubo_c}, Classical={class_c}"
            )
    assert all_costs_match, "TEST 7 FAILED: QUBO and classical costs do not match for all configs"
    print("QUBO/classical costs match: PASS")

    # TEST 8: Minimum QUBO cost must equal minimum classical cost
    assert np.isclose(
        qubo_best_cost, float(classical_best_cost)
    ), f"TEST 8 FAILED: QUBO min cost {qubo_best_cost} != Classical min cost {classical_best_cost}"
    print("Minimum costs match: PASS")

    # TEST 9: Best QUBO configuration must be a valid 4-bit binary configuration
    assert len(qubo_best_config) == 4 and all(
        val in (0, 1) for val in qubo_best_config
    ), f"TEST 9 FAILED: Invalid best configuration {qubo_best_config}"
    print("Best configuration valid: PASS")

    # TEST 10: QUBO solution and classical solution represent the same optimum cost
    qubo_best_classical_cost = calculate_cost(intersections, qubo_best_config)
    assert qubo_best_classical_cost == classical_best_cost, (
        f"TEST 10 FAILED: QUBO best config cost {qubo_best_classical_cost} "
        f"does not equal classical best cost {classical_best_cost}"
    )
    print("QUBO/classical optimum representation: PASS")

    print()
    print("QUBO validation successful.")
    print("=" * 50)


if __name__ == "__main__":
    main()
