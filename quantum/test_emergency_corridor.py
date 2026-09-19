"""Test script and validation suite for Emergency Green Corridor module."""

import sys

# Ensure stdout handles UTF-8 encoding on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from quantum.traffic_model import create_sample_traffic
    from quantum.optimizer import optimize_traffic
    from quantum.emergency_corridor import (
        EmergencyVehicle,
        activate_emergency,
        build_emergency_priority_plan,
        create_green_corridor,
        create_road_network,
        deactivate_emergency,
        derive_signal_directions,
        find_emergency_route,
        is_emergency_active,
    )
except ModuleNotFoundError:
    from traffic_model import create_sample_traffic
    from optimizer import optimize_traffic
    from emergency_corridor import (
        EmergencyVehicle,
        activate_emergency,
        build_emergency_priority_plan,
        create_green_corridor,
        create_road_network,
        deactivate_emergency,
        derive_signal_directions,
        find_emergency_route,
        is_emergency_active,
    )


def main() -> None:
    print("=" * 50)
    print("EMERGENCY GREEN CORRIDOR")
    print("=" * 50)
    print()

    # 1. Create Road Network
    graph = create_road_network()

    # 2. Create Emergency Vehicle Model
    vehicle = EmergencyVehicle(
        vehicle_id="AMB001",
        vehicle_type="Ambulance",
        start_intersection="J1",
        destination_intersection="J4",
        priority="HIGH",
    )

    print("Vehicle:")
    print(vehicle.vehicle_id)
    print()
    print("Type:")
    print(vehicle.vehicle_type)
    print()
    print("Priority:")
    print(vehicle.priority)
    print()
    print("Start:")
    print(vehicle.start_intersection)
    print()
    print("Destination:")
    print(vehicle.destination_intersection)
    print()

    # 3. Find Emergency Route
    route = find_emergency_route(
        graph, vehicle.start_intersection, vehicle.destination_intersection
    )
    print("Calculated route:")
    print(" -> ".join(route))
    print()

    # 4. Create Green Corridor & Signal Priorities
    corridor = create_green_corridor(route)
    signal_directions = derive_signal_directions(route)
    plan = build_emergency_priority_plan(route, signal_directions)

    print("Emergency priority intersections:")
    for inter in corridor:
        print(inter)
    print()

    print("Signal priorities:")
    for inter, direction in signal_directions.items():
        print(f"{inter} -> {direction}")
    print()

    # 5. Activate Emergency State
    state_act = activate_emergency(vehicle, graph)
    active_now = is_emergency_active()
    print("Emergency active:")
    print("YES" if active_now else "NO")
    print()

    # 6. Verify Normal QAOA Optimization still functions during/after emergency
    intersections = create_sample_traffic()
    qaoa_res_during = optimize_traffic(intersections, method="qaoa")

    print("Emergency completed.")
    print()

    # 7. Deactivate Emergency State
    state_deact = deactivate_emergency()
    active_after = is_emergency_active()
    print("Emergency active:")
    print("YES" if active_after else "NO")
    print()

    # 8. Verify Normal QAOA Optimization after emergency deactivation
    qaoa_res_after = optimize_traffic(intersections, method="qaoa")

    # ==================================================
    # VALIDATION / ASSERTIONS
    # ==================================================

    print("=" * 50)
    print("VALIDATION")
    print("=" * 50)

    # TEST 1 & 3: Route calculation
    assert len(route) >= 2, "Route must contain at least 2 nodes"
    print("Route calculation: PASS")

    # TEST 4 & 5: Route endpoints
    assert route[0] == vehicle.start_intersection, "Route must start at vehicle start"
    assert route[-1] == vehicle.destination_intersection, "Route must end at destination"
    print("Route endpoints: PASS")

    # TEST 6 & 7: Green corridor creation
    assert corridor == route, "Green corridor must include all route intersections"
    print("Green corridor creation: PASS")

    # TEST 8: Signal priority plan
    assert set(signal_directions.keys()) == set(route), "Directions must cover route"
    assert all(d in ("NORTH_SOUTH", "EAST_WEST") for d in signal_directions.values())
    print("Signal priority plan: PASS")

    # TEST 9 & 10: Emergency activation
    assert active_now is True, "Emergency must be active after activation"
    print("Emergency activation: PASS")

    # TEST 11 & 12: Emergency deactivation
    assert active_after is False, "Emergency must be inactive after deactivation"
    print("Emergency deactivation: PASS")

    # Normal QAOA works verification
    assert qaoa_res_during["method"] == "qaoa" and len(qaoa_res_during["configuration"]) == 4
    assert qaoa_res_after["method"] == "qaoa" and len(qaoa_res_after["configuration"]) == 4
    print("Normal QAOA still works: PASS")
    print("=" * 50)


if __name__ == "__main__":
    main()
