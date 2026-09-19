"""
integration.py
--------------
Clean data-interface layer for future backend / quantum-optimizer integration.

This module does NOT implement any quantum algorithm.
It provides two layers of functions:

  ── Original simulation helpers (used by main.py) ──
      export_traffic_state()   – full simulation snapshot as a dict
      apply_optimized_timings()– validate & accept timings from an optimizer
      export_to_json()         – write snapshot to simulation_state.json

  ── New public API (for external backend / optimizer programs) ──
      get_traffic_state()      – per-junction metrics dict (vehicles/queue/etc.)
      get_optimizer_input()    – lightweight dict: { junction: vehicle_count }
      apply_optimized_signals()– accept & store signal timings from optimizer
      export_state_to_json()   – save current state to simulation_state.json

Both layers can be used independently.
No extra dependencies beyond the standard library and the project modules.
"""

import json
import os

from metrics import calculate_queue, calculate_waiting_time, calculate_throughput

# ── Module-level defaults ──────────────────────────────────────────────────

DEFAULT_GREEN_TIME = 10   # seconds

# Internal storage for the most recent simulation snapshot.
# External programs can call the public API functions without needing to
# pass simulation objects directly; main.py populates this via
# export_traffic_state() before the demo section runs.
_current_state: dict = {}


# ══════════════════════════════════════════════════════════════════════════════
# ORIGINAL HELPERS  (used by main.py – do not rename or remove)
# ══════════════════════════════════════════════════════════════════════════════

def export_traffic_state(
    traffic,
    signals,
    closed_roads,
    emergency_vehicle=None,
    green_time=DEFAULT_GREEN_TIME,
):
    """
    Build and return a complete snapshot of the current simulation state
    as a plain Python dictionary, and cache it internally so the public
    API functions (get_traffic_state, get_optimizer_input, etc.) can
    serve it to an external caller without extra arguments.

    Args:
        traffic          : { junction: vehicle_count }
        signals          : { junction: signal_state }
        closed_roads     : list of (j1, j2) tuples that have been closed
        emergency_vehicle: EmergencyVehicle instance, or None
        green_time       : green-phase duration in seconds (default 10)

    Returns:
        dict with keys: junctions, signals, closed_roads, emergency
    """
    global _current_state

    state = {}

    # ── Per-junction traffic metrics ───────────────────────────────────────
    junction_data = {}
    for junction, vehicles in traffic.items():
        queue        = calculate_queue(vehicles, green_time)
        waiting_time = calculate_waiting_time(queue)
        throughput   = calculate_throughput(vehicles, queue)

        junction_data[junction] = {
            "vehicles"    : vehicles,
            "queue"       : queue,
            "waiting_time": waiting_time,
            "throughput"  : throughput,
        }

    state["junctions"] = junction_data

    # ── Signal states ──────────────────────────────────────────────────────
    state["signals"] = dict(signals)   # shallow copy so the caller's dict is safe

    # ── Closed roads ───────────────────────────────────────────────────────
    state["closed_roads"] = [list(road) for road in closed_roads]

    # ── Emergency status ───────────────────────────────────────────────────
    if emergency_vehicle is not None:
        state["emergency"] = {
            "detected"   : True,
            "active"     : emergency_vehicle.active,
            "source"     : emergency_vehicle.source,
            "destination": emergency_vehicle.destination,
            "route"      : emergency_vehicle.route,
        }
    else:
        state["emergency"] = {
            "detected"   : False,
            "active"     : False,
            "source"     : None,
            "destination": None,
            "route"      : [],
        }

    # Cache for the public API
    _current_state = state

    return state


def apply_optimized_timings(timings):
    """
    Accept a dict of optimized green-time values from a backend / quantum
    optimizer, validate each entry, and return the validated dict.

    This is the original helper kept for backward-compatibility.
    New code should prefer apply_optimized_signals().

    Args:
        timings : { junction_name: green_time_seconds }
                  Example: { "J1": 15, "J2": 25, "J3": 10, "J4": 20 }

    Returns:
        dict of validated timings, or {} on error.
    """
    return apply_optimized_signals(timings, _print_header=False)


def export_to_json(state, filepath="simulation_state.json"):
    """
    Write the simulation state dictionary to a JSON file.

    Args:
        state    : dict returned by export_traffic_state()
        filepath : output file path (default: simulation_state.json)
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)
        print(f"\n💾 Simulation state saved → {os.path.abspath(filepath)}")
    except OSError as e:
        print(f"❌ Failed to write JSON: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC API  (for external backend / quantum optimizer programs)
# ══════════════════════════════════════════════════════════════════════════════

def get_traffic_state():
    """
    Return per-junction traffic metrics from the most recent simulation run.

    This is the primary read-interface for an external backend or optimizer.
    Call this after main.py has finished (or import and call it from your
    own script after running the simulator).

    Returns:
        dict  –  Example:
            {
                "J1": {"vehicles": 8,  "queue": 0, "waiting_time": 0,  "throughput": 8},
                "J2": {"vehicles": 23, "queue": 3, "waiting_time": 6,  "throughput": 20},
                "J3": {"vehicles": 24, "queue": 4, "waiting_time": 8,  "throughput": 20},
                "J4": {"vehicles": 13, "queue": 0, "waiting_time": 0,  "throughput": 13},
            }
        Returns {} if the simulator has not been run yet.
    """
    if not _current_state:
        print("⚠️  get_traffic_state: no simulation data available yet.")
        return {}

    # Return a deep copy so callers cannot mutate the cached state
    return {
        junction: dict(metrics)
        for junction, metrics in _current_state.get("junctions", {}).items()
    }


def get_optimizer_input():
    """
    Return a lightweight dict containing only vehicle counts per junction.
    This is the minimal data an optimizer needs to compute signal timings.

    Returns:
        dict  –  Example:
            { "J1": 8, "J2": 23, "J3": 24, "J4": 13 }
        Returns {} if no simulation data is available.
    """
    traffic_state = get_traffic_state()
    if not traffic_state:
        return {}

    return {junction: data["vehicles"] for junction, data in traffic_state.items()}


def apply_optimized_signals(signal_timings, _print_header=True):
    """
    Accept and validate optimized signal timing values from an external
    backend or quantum optimizer.  Stores the timings internally and
    returns the validated dict so the simulator can apply them.

    This function is intentionally a thin wrapper — the actual optimization
    algorithm lives in the optimizer module (another team member's code).

    Args:
        signal_timings : dict  { junction_name: green_time_seconds }
                         Example: { "J1": 15, "J2": 25, "J3": 10, "J4": 20 }
        _print_header  : internal flag; keep True for normal usage.

    Returns:
        dict of validated timings, or {} on bad input.
    """
    if not isinstance(signal_timings, dict):
        print(
            "⚠️  apply_optimized_signals: expected a dict, "
            f"received: {type(signal_timings)}"
        )
        return {}

    validated = {}
    for junction, green_time in signal_timings.items():
        if not isinstance(green_time, (int, float)) or green_time <= 0:
            print(
                f"⚠️  Invalid green time for {junction}: {green_time}. Skipping."
            )
            continue
        validated[junction] = green_time

    if _print_header:
        print("\n✅ Optimized signal timings accepted:")
        for junction, t in validated.items():
            print(f"   {junction}: {t} sec")

    # Store in state cache so export_state_to_json() can include them
    if _current_state:
        _current_state["optimized_signal_timings"] = validated

    return validated


def export_state_to_json(filepath="simulation_state.json"):
    """
    Save the current simulation state (including any optimized timings)
    to a JSON file.  This is the public-API version of export_to_json();
    it uses the internally cached state so no arguments are required.

    Args:
        filepath : output path (default: simulation_state.json)

    Returns:
        True on success, False on failure.
    """
    if not _current_state:
        print("⚠️  export_state_to_json: no state to export.")
        return False

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(_current_state, f, indent=4)
        print(f"💾 State exported → {os.path.abspath(filepath)}")
        return True
    except OSError as e:
        print(f"❌ export_state_to_json failed: {e}")
        return False
