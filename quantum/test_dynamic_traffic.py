"""Test suite demonstrating dynamic traffic inputs, validation, and adaptive optimization."""

import sys
import numpy as np

# Ensure stdout handles UTF-8 encoding on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from quantum.traffic_model import create_traffic_from_dicts
    from quantum.optimizer import optimize_traffic_from_dicts
except ModuleNotFoundError:
    from traffic_model import create_traffic_from_dicts
    from optimizer import optimize_traffic_from_dicts


def main() -> None:
    print("=" * 60)
    print("DYNAMIC TRAFFIC OPTIMIZATION & ADAPTIVE SCENARIOS")
    print("=" * 60)
    print()

    # ----------------------------------------------------
    # SCENARIO 1: Normal Balanced Traffic
    # ----------------------------------------------------
    scenario_1_data = [
        {"name": "J1", "north": 20, "south": 15, "east": 35, "west": 30},
        {"name": "J2", "north": 40, "south": 25, "east": 15, "west": 20},
        {"name": "J3", "north": 10, "south": 20, "east": 45, "west": 40},
        {"name": "J4", "north": 30, "south": 35, "east": 25, "west": 15},
    ]

    # ----------------------------------------------------
    # SCENARIO 2: Heavy North-South Traffic Surge
    # ----------------------------------------------------
    scenario_2_data = [
        {"name": "J1", "north": 70, "south": 80, "east": 20, "west": 15},
        {"name": "J2", "north": 90, "south": 85, "east": 10, "west": 15},
        {"name": "J3", "north": 60, "south": 65, "east": 25, "west": 20},
        {"name": "J4", "north": 80, "south": 75, "east": 15, "west": 20},
    ]

    # ----------------------------------------------------
    # SCENARIO 3: Heavy East-West Traffic Surge
    # ----------------------------------------------------
    scenario_3_data = [
        {"name": "J1", "north": 10, "south": 15, "east": 80, "west": 90},
        {"name": "J2", "north": 15, "south": 20, "east": 85, "west": 75},
        {"name": "J3", "north": 10, "south": 10, "east": 90, "west": 95},
        {"name": "J4", "north": 20, "south": 15, "east": 70, "west": 80},
    ]

    scenarios = [
        ("SCENARIO 1: Normal Balanced Traffic", scenario_1_data),
        ("SCENARIO 2: North-South Traffic Surge", scenario_2_data),
        ("SCENARIO 3: East-West Traffic Surge", scenario_3_data),
    ]

    scenario_results = []

    for name, data in scenarios:
        print(f"--- {name} ---")
        intersections = create_traffic_from_dicts(data)
        for inter in intersections:
            print(
                f"  {inter.name}: N={inter.north}, S={inter.south}, E={inter.east}, W={inter.west} "
                f"| NS_Pressure={inter.north_south_pressure}, EW_Pressure={inter.east_west_pressure}"
            )

        class_res = optimize_traffic_from_dicts(data, method="classical")
        qaoa_res = optimize_traffic_from_dicts(data, method="qaoa")

        matched = (class_res["configuration"] == qaoa_res["configuration"]) and np.isclose(
            class_res["cost"], qaoa_res["cost"]
        )
        match_str = "YES" if matched else "NO"

        print(f"  Classical Optimum -> Config: {class_res['configuration']} | Cost: {class_res['cost']}")
        print(f"  QAOA Optimum      -> Config: {qaoa_res['configuration']} | Cost: {qaoa_res['cost']}")
        print(f"  QAOA matched classical: {match_str}")
        print()

        scenario_results.append(
            {
                "name": name,
                "classical_config": class_res["configuration"],
                "classical_cost": class_res["cost"],
                "qaoa_config": qaoa_res["configuration"],
                "qaoa_cost": qaoa_res["cost"],
                "matched": match_str,
            }
        )

    # Summary table
    print("=" * 60)
    print("SCENARIOS SUMMARY TABLE")
    print("=" * 60)
    print(f"{'Scenario':<36} {'Classical':<14} {'QAOA':<14} {'Match':<6}")
    print("-" * 72)
    for sres in scenario_results:
        print(
            f"{sres['name'][:34]:<36} {str(sres['classical_config']):<14} "
            f"{str(sres['qaoa_config']):<14} {sres['matched']:<6}"
        )
    print("=" * 60)
    print()

    # ==================================================
    # ASSERTIONS & INPUT VALIDATIONS
    # ==================================================
    print("=" * 60)
    print("VALIDATION TESTS")
    print("=" * 60)

    # 1. Valid traffic data creates exactly 4 intersections
    created = create_traffic_from_dicts(scenario_1_data)
    assert len(created) == 4, "TEST 1 FAILED: Expected 4 intersections"
    print("1. Valid traffic data creates exactly 4 intersections: PASS")

    # 2. Negative traffic values rejected
    neg_data = [dict(item) for item in scenario_1_data]
    neg_data[0]["north"] = -5
    try:
        create_traffic_from_dicts(neg_data)
        assert False, "Should reject negative traffic values"
    except ValueError as e:
        assert "cannot be negative" in str(e)
        print("2. Negative traffic values rejected: PASS")

    # 3. Missing fields rejected
    missing_data = [dict(item) for item in scenario_1_data]
    del missing_data[0]["west"]
    try:
        create_traffic_from_dicts(missing_data)
        assert False, "Should reject missing fields"
    except ValueError as e:
        assert "missing required fields" in str(e)
        print("3. Missing fields rejected: PASS")

    # 4. Duplicate intersection names rejected
    dup_data = [dict(item) for item in scenario_1_data]
    dup_data[1]["name"] = "J1"
    try:
        create_traffic_from_dicts(dup_data)
        assert False, "Should reject duplicate names"
    except ValueError as e:
        assert "Duplicate intersection name" in str(e)
        print("4. Duplicate intersection names rejected: PASS")

    # 5. More or fewer than 4 intersections rejected
    try:
        create_traffic_from_dicts(scenario_1_data[:3])
        assert False, "Should reject fewer than 4 intersections"
    except ValueError as e:
        assert "Exactly 4 intersections are required" in str(e)
        print("5. Non-4 intersection count rejected: PASS")

    # 6. Dynamic traffic data can be passed into optimizer
    res_dyn = optimize_traffic_from_dicts(scenario_2_data, method="classical")
    assert res_dyn["method"] == "classical"
    print("6. Dynamic traffic passed into optimizer: PASS")

    # 7. Returned configuration has exactly 4 bits
    assert len(res_dyn["configuration"]) == 4
    print("7. Returned configuration length (4 bits): PASS")

    # 8. Every configuration bit is 0 or 1
    assert all(b in (0, 1) for b in res_dyn["configuration"])
    print("8. Every configuration bit is 0 or 1: PASS")

    # 9. Returned cost is numeric
    assert isinstance(res_dyn["cost"], (int, float))
    print("9. Returned cost is numeric: PASS")

    # 10. Both classical and QAOA process dynamic traffic input
    qaoa_dyn = optimize_traffic_from_dicts(scenario_3_data, method="qaoa")
    assert qaoa_dyn["method"] == "qaoa" and len(qaoa_dyn["configuration"]) == 4
    print("10. Classical and QAOA process dynamic traffic: PASS")

    print()
    print("All 10 validation tests passed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
