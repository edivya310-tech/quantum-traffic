"""Test script and assertions for Classical Brute-Force Traffic Optimizer."""

import sys

# Ensure stdout handles UTF-8 encoding on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from quantum.traffic_model import create_sample_traffic
    from quantum.classical_optimizer import calculate_cost, optimize_traffic
except ModuleNotFoundError:
    from traffic_model import create_sample_traffic
    from classical_optimizer import calculate_cost, optimize_traffic


def main() -> None:
    # 1. Create sample traffic network (J1, J2, J3, J4)
    intersections = create_sample_traffic()

    # 2. Run the classical brute-force optimizer
    result = optimize_traffic(intersections)

    evaluations = result["evaluations"]
    best_config = result["best_configuration"]
    best_cost = result["best_cost"]

    # 3. Print every one of the 16 configurations and their costs
    for item in evaluations:
        config = item["configuration"]
        cost = item["cost"]
        print(f"Configuration {config} -> Cost: {cost}")

    print()
    print(f"Best configuration: {best_config}")
    print(f"Best cost: {best_cost}")

    # ==================================================
    # TESTS / ASSERTIONS
    # ==================================================

    # 1. Exactly 16 configurations were evaluated.
    assert len(evaluations) == 16, f"Expected 16 evaluations, got {len(evaluations)}"

    # 2. Every configuration contains exactly 4 values.
    for item in evaluations:
        assert len(item["configuration"]) == 4, (
            f"Configuration length must be 4: {item['configuration']}"
        )

    # 3. Every value is either 0 or 1.
    for item in evaluations:
        for val in item["configuration"]:
            assert val in (0, 1), f"Configuration value must be 0 or 1: {val}"

    # 4. Every configuration is unique.
    unique_configs = set(tuple(item["configuration"]) for item in evaluations)
    assert len(unique_configs) == 16, "Not all 16 configurations were unique"

    # 5. The reported best cost equals the minimum of all evaluated costs.
    min_evaluated_cost = min(item["cost"] for item in evaluations)
    assert best_cost == min_evaluated_cost, (
        f"Best cost {best_cost} does not match minimum evaluated cost {min_evaluated_cost}"
    )

    # 6. The reported best configuration actually produces the reported best cost when passed to calculate_cost().
    computed_best_cost = calculate_cost(intersections, best_config)
    assert computed_best_cost == best_cost, (
        f"calculate_cost({best_config}) produced {computed_best_cost}, expected {best_cost}"
    )

    # 7. The optimizer does not return an invalid configuration.
    assert len(best_config) == 4, "Best configuration must have 4 elements"
    assert all(val in (0, 1) for val in best_config), "Best configuration values must be 0 or 1"

    print("\nAll 7 assertions passed successfully!")


if __name__ == "__main__":
    main()
