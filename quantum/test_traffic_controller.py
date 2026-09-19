"""Test suite and validation checks for TrafficController orchestration module."""

import json
import sys

# Ensure stdout handles UTF-8 encoding on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from quantum.traffic_controller import TrafficController
except ModuleNotFoundError:
    from traffic_controller import TrafficController


def main() -> None:
    print("=" * 60)
    print("TRAFFIC CONTROLLER ORCHESTRATION TESTS")
    print("=" * 60)
    print()

    sample_traffic = [
        {"name": "J1", "north": 20, "south": 15, "east": 35, "west": 30},
        {"name": "J2", "north": 40, "south": 25, "east": 15, "west": 20},
        {"name": "J3", "north": 10, "south": 20, "east": 45, "west": 40},
        {"name": "J4", "north": 30, "south": 35, "east": 25, "west": 15},
    ]

    emergency_payload = {
        "vehicle_id": "AMB-01",
        "vehicle_type": "ambulance",
        "start_intersection": "J1",
        "destination_intersection": "J4",
        "priority": "HIGH",
    }

    # ==================================================
    # TEST 1: Classical Mode Controller
    # ==================================================
    ctrl_class = TrafficController(method="classical")
    ctrl_class.update_traffic(sample_traffic)
    res_class = ctrl_class.compute_control_plan()

    assert res_class["mode"] == "normal", "TEST 1 FAILED: Expected mode 'normal'"
    assert (
        res_class["method"] == "classical"
    ), "TEST 1 FAILED: Expected method 'classical'"
    assert (
        len(res_class["configuration"]) == 4
    ), "TEST 1 FAILED: Configuration length != 4"
    assert "cost" in res_class, "TEST 1 FAILED: Missing 'cost'"

    # Verify JSON serializability
    json_class_str = json.dumps(res_class)
    assert len(json_class_str) > 0
    print("TEST 1: Classical mode normal control plan: PASS")

    # ==================================================
    # TEST 2: QAOA Mode Controller
    # ==================================================
    ctrl_qaoa = TrafficController(method="qaoa")
    ctrl_qaoa.update_traffic(sample_traffic)
    res_qaoa = ctrl_qaoa.compute_control_plan()

    assert res_qaoa["mode"] == "normal", "TEST 2 FAILED: Expected mode 'normal'"
    assert res_qaoa["method"] == "qaoa", "TEST 2 FAILED: Expected method 'qaoa'"
    assert (
        len(res_qaoa["configuration"]) == 4
    ), "TEST 2 FAILED: Configuration length != 4"
    assert "cost" in res_qaoa, "TEST 2 FAILED: Missing 'cost'"

    # Verify JSON serializability
    json_qaoa_str = json.dumps(res_qaoa)
    assert len(json_qaoa_str) > 0
    print("TEST 2: QAOA mode normal control plan: PASS")

    # ==================================================
    # TEST 3: Activate Emergency Corridor
    # ==================================================
    em_plan = ctrl_qaoa.activate_emergency(emergency_payload)

    assert em_plan["mode"] == "emergency", "TEST 3 FAILED: Expected mode 'emergency'"
    assert (
        em_plan["vehicle_id"] == "AMB-01"
    ), "TEST 3 FAILED: Vehicle ID mismatch"
    assert em_plan["route"][0] == "J1", "TEST 3 FAILED: Route start mismatch"
    assert (
        em_plan["route"][-1] == "J4"
    ), "TEST 3 FAILED: Route destination mismatch"
    assert len(em_plan["green_corridor"]) > 0, "TEST 3 FAILED: Empty green corridor"
    assert "priority_plan" in em_plan, "TEST 3 FAILED: Missing priority plan"

    json_em_str = json.dumps(em_plan)
    assert len(json_em_str) > 0
    print("TEST 3: Ambulance emergency activation: PASS")

    # ==================================================
    # TEST 4: Emergency Override Rule
    # ==================================================
    status_em = ctrl_qaoa.get_status()
    assert status_em["emergency_active"] is True
    assert status_em["emergency_vehicle_id"] == "AMB-01"

    override_plan = ctrl_qaoa.compute_control_plan()
    assert (
        override_plan["mode"] == "emergency"
    ), "TEST 4 FAILED: Emergency override failed"
    assert "configuration" not in override_plan
    print("TEST 4: Emergency override rule (prevents normal QAOA): PASS")

    # ==================================================
    # TEST 5: Deactivate Emergency & Return to Normal
    # ==================================================
    ctrl_qaoa.deactivate_emergency()
    status_norm = ctrl_qaoa.get_status()
    assert status_norm["emergency_active"] is False

    res_post_em = ctrl_qaoa.compute_control_plan()
    assert (
        res_post_em["mode"] == "normal"
    ), "TEST 5 FAILED: Did not return to normal mode"
    assert len(res_post_em["configuration"]) == 4
    print("TEST 5: Deactivate emergency & return to normal optimization: PASS")

    # ==================================================
    # TEST 6: Invalid Method Handling
    # ==================================================
    try:
        TrafficController(method="invalid_method")
        assert False, "Should raise ValueError for invalid method"
    except ValueError as e:
        assert "method must be 'classical' or 'qaoa'" in str(e)
        print("TEST 6: Invalid optimization method rejected: PASS")

    # ==================================================
    # TEST 7: Missing/Invalid Traffic Data Handling
    # ==================================================
    empty_ctrl = TrafficController(method="qaoa")
    try:
        empty_ctrl.compute_control_plan()
        assert False, "Should raise ValueError when computing plan without traffic"
    except ValueError as e:
        assert "No traffic data loaded" in str(e)
        print("TEST 7: Unloaded traffic plan request rejected: PASS")

    # ==================================================
    # TEST 8: JSON Serialization Verification
    # ==================================================
    for mode_name, plan_dict in [
        ("Normal Classical", res_class),
        ("Normal QAOA", res_qaoa),
        ("Emergency Plan", em_plan),
    ]:
        try:
            dumped = json.dumps(plan_dict)
            reloaded = json.loads(dumped)
            assert reloaded["mode"] in ("normal", "emergency")
        except Exception as err:
            assert False, f"JSON serialization failed for {mode_name}: {err}"
    print("TEST 8: 100% JSON serialization verification across all modes: PASS")

    print()
    print("All 8 TrafficController test assertions passed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
