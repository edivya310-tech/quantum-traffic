"""Hackathon Demonstration Script for Quantum-Enhanced Adaptive Urban Traffic Optimization."""

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
    print("=" * 65)
    print(" HACKATHON DEMO: QUANTUM-ENHANCED URBAN TRAFFIC CONTROLLER")
    print("=" * 65)
    print()

    # Initialize TrafficController using QAOA quantum optimization
    controller = TrafficController(method="qaoa", p=1, shots=1024)

    # ----------------------------------------------------
    # SECTION A: NORMAL TRAFFIC INGESTION
    # ----------------------------------------------------
    print("=== NORMAL TRAFFIC ===")
    sample_traffic = [
        {"name": "J1", "north": 20, "south": 15, "east": 35, "west": 30},
        {"name": "J2", "north": 40, "south": 25, "east": 15, "west": 20},
        {"name": "J3", "north": 10, "south": 20, "east": 45, "west": 40},
        {"name": "J4", "north": 30, "south": 35, "east": 25, "west": 15},
    ]

    controller.update_traffic(sample_traffic)
    status = controller.get_status()
    print("Current Controller Status:")
    print(json.dumps(status, indent=2))
    print()

    # ----------------------------------------------------
    # SECTION B: TRAFFIC OPTIMIZATION (QAOA & QUBO)
    # ----------------------------------------------------
    print("=== OPTIMIZATION RESULT ===")
    normal_plan = controller.compute_control_plan()
    print("Computed Control Plan (QAOA Quantum Optimization):")
    print(json.dumps(normal_plan, indent=2))
    print()

    # ----------------------------------------------------
    # SECTION C: AMBULANCE EMERGENCY ACTIVATION
    # ----------------------------------------------------
    print("=== AMBULANCE EMERGENCY ===")
    ambulance_payload = {
        "vehicle_id": "AMB-01",
        "vehicle_type": "ambulance",
        "start_intersection": "J1",
        "destination_intersection": "J4",
        "priority": "HIGH",
    }
    print("Incoming Emergency Event Payload:")
    print(json.dumps(ambulance_payload, indent=2))
    print()

    # ----------------------------------------------------
    # SECTION D: EMERGENCY GREEN CORRIDOR OVERRIDE
    # ----------------------------------------------------
    print("=== EMERGENCY GREEN CORRIDOR ===")
    emergency_plan = controller.activate_emergency(ambulance_payload)
    print("Active Emergency Control Plan (Pre-empts Normal Optimization):")
    print(json.dumps(emergency_plan, indent=2))
    print()

    active_status = controller.get_status()
    print("Controller Status During Emergency:")
    print(json.dumps(active_status, indent=2))
    print()

    # ----------------------------------------------------
    # SECTION E & F: EMERGENCY DEACTIVATION & RETURN TO NORMAL
    # ----------------------------------------------------
    print("=== RETURN TO NORMAL ===")
    controller.deactivate_emergency()
    print("Emergency corridor deactivated. System restored to normal mode.")
    print()

    post_emergency_plan = controller.compute_control_plan()
    print("Post-Emergency Control Plan (Resumed QAOA Traffic Optimization):")
    print(json.dumps(post_emergency_plan, indent=2))
    print()

    print("=" * 65)
    print(" HACKATHON DEMO COMPLETED SUCCESSFULLY")
    print("=" * 65)


if __name__ == "__main__":
    main()
