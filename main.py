"""
main.py
-------
Traffic Emergency Simulator – complete simulation entry-point.

Run with:
    python main.py

Simulation order
----------------
 1.  Create road network
 2.  Generate traffic
 3.  Display traffic
 4.  Apply traffic surge at J3
 5.  Close road J1-J3
 6.  Calculate traffic metrics
 7.  Display metrics
 8.  Detect an emergency vehicle (J1 → J4)
 9.  Find emergency route
10.  Activate green corridor
11.  Simulate emergency vehicle movement
12.  Reach destination
13.  Deactivate emergency mode
14.  Restore signals
15.  Export simulation state to JSON
16.  Print final summary
"""

import sys
import io

# Ensure UTF-8 output on Windows terminals that default to cp1252
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from network     import create_network
from traffic     import generate_vehicles
from events      import traffic_surge, road_closure
from metrics     import calculate_queue, calculate_waiting_time, calculate_throughput
from emergency   import EmergencyVehicle, init_signals, display_signals, format_route
from integration import (
    export_traffic_state,
    export_to_json,
    get_traffic_state,
    get_optimizer_input,
    apply_optimized_signals,
    export_state_to_json,
)

# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 – Create Road Network
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 40)
print("🚦 TRAFFIC NETWORK")
print("=" * 40)

road_network = create_network()

print("Junctions:", list(road_network.nodes))
print("Roads    :", list(road_network.edges))


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 & 3 – Generate and Display Traffic
# ══════════════════════════════════════════════════════════════════════════════

traffic = generate_vehicles(road_network.nodes)

print("\n" + "=" * 40)
print("🚗 INITIAL TRAFFIC")
print("=" * 40)

for junction, vehicles in traffic.items():
    print(f"  {junction}: {vehicles} vehicles")


# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 – Traffic Surge at J3  (applied exactly once)
# ══════════════════════════════════════════════════════════════════════════════

traffic_surge(traffic, "J3")

print("\n" + "=" * 40)
print("🚨 TRAFFIC SURGE at J3")
print("=" * 40)

for junction, vehicles in traffic.items():
    print(f"  {junction}: {vehicles} vehicles")


# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 – Close Road J1-J3
# ══════════════════════════════════════════════════════════════════════════════

closed_roads = [("J1", "J3")]          # track closed roads for reporting
road_closure(road_network, ("J1", "J3"))

print("\n" + "=" * 40)
print("🚧 ROAD CLOSURE")
print("=" * 40)
print("  Closed road  : J1 ↔ J3")
print("  Available roads:", list(road_network.edges))


# ══════════════════════════════════════════════════════════════════════════════
# STEP 6 & 7 – Calculate and Display Traffic Metrics
# ══════════════════════════════════════════════════════════════════════════════

GREEN_TIME = 10   # seconds – used throughout this simulation

# Build metrics dict for re-use in summary and JSON export
metrics = {}
for junction, vehicles in traffic.items():
    q  = calculate_queue(vehicles, GREEN_TIME)
    wt = calculate_waiting_time(q)
    tp = calculate_throughput(vehicles, q)
    metrics[junction] = {
        "vehicles"    : vehicles,
        "queue"       : q,
        "waiting_time": wt,
        "throughput"  : tp,
    }

print("\n" + "=" * 40)
print("📊 TRAFFIC METRICS")
print("=" * 40)

for junction, m in metrics.items():
    print(f"\n  {junction}")
    print(f"    Vehicles     : {m['vehicles']}")
    print(f"    Queue        : {m['queue']}")
    print(f"    Waiting Time : {m['waiting_time']} sec")
    print(f"    Throughput   : {m['throughput']}")


# ══════════════════════════════════════════════════════════════════════════════
# STEP 8 – Detect Emergency Vehicle
# ══════════════════════════════════════════════════════════════════════════════

# Initialise all junction signals to NORMAL
signals = init_signals(road_network.nodes)

print("\n" + "=" * 40)
print("🚑 EMERGENCY DETECTED")
print("=" * 40)
print("  Source      : J1")
print("  Destination : J4")

emergency = EmergencyVehicle(source="J1", destination="J4")


# ══════════════════════════════════════════════════════════════════════════════
# STEP 9 – Find Emergency Route
# ══════════════════════════════════════════════════════════════════════════════

route = emergency.find_route(road_network)

print("\n  Emergency Route:")
if route:
    print(f"  {format_route(route)}")
else:
    print("  ❌ No route available – simulation cannot continue.")
    exit(1)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 10 – Activate Green Corridor
# ══════════════════════════════════════════════════════════════════════════════

emergency.activate(signals)

print("\n" + "=" * 40)
print("🚦 GREEN CORRIDOR ACTIVATED")
print("=" * 40)

display_signals(signals)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 11 & 12 – Simulate Emergency Vehicle Movement
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 40)
print("🚑 VEHICLE MOVEMENT SIMULATION")
print("=" * 40)

emergency.simulate_movement(signals)

print("  🏁 Emergency vehicle reached destination:", emergency.destination)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 13 & 14 – Deactivate Emergency Mode, Restore Signals
# ══════════════════════════════════════════════════════════════════════════════

emergency.deactivate(signals)

print("\n" + "=" * 40)
print("🚑 EMERGENCY COMPLETED")
print("=" * 40)
print("\n🚦 Returning signals to NORMAL\n")

display_signals(signals)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 15 – Export Simulation State to JSON
# ══════════════════════════════════════════════════════════════════════════════

state = export_traffic_state(
    traffic         = traffic,
    signals         = signals,
    closed_roads    = closed_roads,
    emergency_vehicle = emergency,
    green_time      = GREEN_TIME,
)

export_to_json(state, "simulation_state.json")


# ══════════════════════════════════════════════════════════════════════════════
# STEP 16 – Final Summary
# ══════════════════════════════════════════════════════════════════════════════

total_vehicles = sum(m["vehicles"]     for m in metrics.values())
total_queued   = sum(m["queue"]        for m in metrics.values())
total_tp       = sum(m["throughput"]   for m in metrics.values())
avg_wait       = (
    sum(m["waiting_time"] for m in metrics.values()) / len(metrics)
    if metrics else 0
)

print("\n" + "=" * 40)
print("📋 TRAFFIC SIMULATION SUMMARY")
print("=" * 40)
print(f"  Total vehicles      : {total_vehicles}")
print(f"  Total queued        : {total_queued}")
print(f"  Average waiting time: {avg_wait:.1f} sec")
print(f"  Total throughput    : {total_tp}")

print(f"\n  Emergency           : {'Detected' if emergency else 'Not Detected'}")
print(f"  Emergency route     : {format_route(emergency.route)}")

closed_str = ", ".join(f"{r[0]} ↔ {r[1]}" for r in closed_roads) if closed_roads else "None"
print(f"  Road closures       : {closed_str}")

signal_mode = "EMERGENCY" if emergency.active else "NORMAL"
print(f"  Signal mode         : {signal_mode}")
print("=" * 40)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 17 – Backend / Quantum Optimizer Integration Demo
# (interface demonstration only – no real quantum algorithm runs here)
# ══════════════════════════════════════════════════════════════════════════════

print("\n\n" + "=" * 40)
print("🔗 BACKEND / QUANTUM OPTIMIZER INTERFACE")
print("=" * 40)
print("""
  ┌─────────────────────────┐
  │   Traffic Simulator     │
  └────────────┬────────────┘
               │  get_optimizer_input()
               ▼
  ┌─────────────────────────┐
  │    Optimizer Input      │
  │  { junction: vehicles } │
  └────────────┬────────────┘
               │  [Backend / Quantum Optimizer]
               ▼
  ┌─────────────────────────┐
  │  Optimized Signal       │
  │  Timings (green secs)   │
  └────────────┬────────────┘
               │  apply_optimized_signals()
               ▼
  ┌─────────────────────────┐
  │   Traffic Simulator     │
  │   (updated timings)     │
  └─────────────────────────┘
""")

# ── A) Read current traffic state (full metrics) ───────────────────────────
print("── A) Current Traffic State (get_traffic_state()) ──────────────────")
traffic_state = get_traffic_state()
for junction, data in traffic_state.items():
    print(
        f"  {junction}:  vehicles={data['vehicles']:3d}  "
        f"queue={data['queue']:3d}  "
        f"wait={data['waiting_time']:4d}s  "
        f"throughput={data['throughput']:3d}"
    )

# ── B) Get lightweight optimizer input ────────────────────────────────────
print("\n── B) Optimizer Input (get_optimizer_input()) ───────────────────────")
optimizer_input = get_optimizer_input()
print("  Sending to optimizer:", optimizer_input)

# ── C) Simulated optimizer response (placeholder – replace with real call) ─
print("\n── C) Backend / Quantum Optimizer ───────────────────────────────────")
print("  [Optimizer would process the above vehicle counts here]")
print("  [Returning optimized green-time allocations ...]")

# These values would come from the real optimizer module.
# Substitute this dict with the output of your quantum/ML solver.
simulated_optimizer_output = {
    "J1": 12,
    "J2": 20,
    "J3": 35,   # longer green for the surged junction
    "J4": 13,
}
print("  Optimizer response:", simulated_optimizer_output)

# ── D) Apply optimized signal timings back to the simulator ───────────────
print("\n── D) Apply Optimized Signals (apply_optimized_signals()) ──────────")
validated_timings = apply_optimized_signals(simulated_optimizer_output)

# ── E) Export updated state to JSON ───────────────────────────────────────
print("\n── E) Export Updated State (export_state_to_json()) ─────────────────")
export_state_to_json("simulation_state.json")

print("\n" + "=" * 40)
print("✅ Integration interface demo complete.")
print("   Replace 'simulated_optimizer_output' above with your")
print("   real backend / quantum optimizer call.")
print("=" * 40)