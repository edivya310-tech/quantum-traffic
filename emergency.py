"""
emergency.py
------------
Handles emergency vehicle detection, routing, green corridor
activation, movement simulation, and deactivation.
"""

import networkx as nx


# ── Signal State Constants ─────────────────────────────────────────────────

SIGNAL_NORMAL = "NORMAL"
SIGNAL_GREEN  = "GREEN"
SIGNAL_RED    = "RED"


# ── Signal Manager ─────────────────────────────────────────────────────────

def init_signals(junctions):
    """
    Create a signal-state dict for every junction, defaulting to NORMAL.

    Args:
        junctions: iterable of junction names (e.g. ['J1', 'J2', 'J3', 'J4'])

    Returns:
        dict  { 'J1': 'NORMAL', 'J2': 'NORMAL', ... }
    """
    return {j: SIGNAL_NORMAL for j in junctions}


def set_signal(signals, junction, state):
    """
    Set the signal state for a single junction.

    Args:
        signals  : the signal-state dict
        junction : junction name string
        state    : one of SIGNAL_NORMAL / SIGNAL_GREEN / SIGNAL_RED
    """
    if junction not in signals:
        print(f"⚠️  Warning: Junction '{junction}' not found in signal map.")
        return
    signals[junction] = state


def activate_green_corridor(signals, route):
    """
    Set every junction in *route* to GREEN; all others stay unchanged.

    Args:
        signals : the signal-state dict
        route   : list of junction names that form the emergency route
    """
    for junction in route:
        set_signal(signals, junction, SIGNAL_GREEN)


def restore_signals(signals):
    """
    Reset all junctions back to NORMAL (called after emergency ends).

    Args:
        signals : the signal-state dict  (modified in-place)
    """
    for junction in signals:
        signals[junction] = SIGNAL_NORMAL


def display_signals(signals):
    """Print the current signal state for every junction."""
    for junction, state in signals.items():
        print(f"  {junction}: {state}")


# ── Emergency Vehicle ──────────────────────────────────────────────────────

class EmergencyVehicle:
    """
    Represents one emergency vehicle travelling through the road network.

    Attributes:
        source      : starting junction
        destination : target junction
        route       : computed list of junctions, or [] if none found
        active      : True while the vehicle is still en-route
    """

    def __init__(self, source, destination):
        self.source      = source
        self.destination = destination
        self.route       = []    # filled by find_route()
        self.active      = False

    # ── Route Finding ──────────────────────────────────────────────────────

    def find_route(self, road_network):
        """
        Use NetworkX shortest_path to find a route on the *current* graph.

        Closed roads are already removed from road_network before this call,
        so the path automatically respects closures.

        Returns:
            list of junctions, or [] if no path exists / invalid junctions.
        """
        # Validate that both junctions exist in the network
        if self.source not in road_network.nodes:
            print(f"❌ Error: Source junction '{self.source}' does not exist.")
            return []

        if self.destination not in road_network.nodes:
            print(f"❌ Error: Destination junction '{self.destination}' does not exist.")
            return []

        try:
            path = nx.shortest_path(
                road_network,
                source=self.source,
                target=self.destination
            )
            self.route = path
            return path

        except nx.NetworkXNoPath:
            print(
                f"❌ No route available from {self.source} to "
                f"{self.destination} (roads may be closed)."
            )
            self.route = []
            return []

        except nx.NodeNotFound as e:
            print(f"❌ Node error: {e}")
            self.route = []
            return []

    # ── Emergency Activation / Deactivation ───────────────────────────────

    def activate(self, signals):
        """
        Mark the vehicle as active and set the green corridor on *signals*.
        Call find_route() first so self.route is populated.
        """
        if not self.route:
            print("⚠️  Cannot activate emergency: no valid route found.")
            return

        self.active = True
        activate_green_corridor(signals, self.route)

    def deactivate(self, signals):
        """
        Mark the vehicle as inactive and restore all signals to NORMAL.
        """
        self.active = False
        restore_signals(signals)

    # ── Movement Simulation ───────────────────────────────────────────────

    def simulate_movement(self, signals):
        """
        Step through each junction in the route and print the signal state
        at that moment.  Keeps the simulation simple and text-based.

        Args:
            signals : current signal-state dict (green corridor already active)
        """
        if not self.route:
            print("⚠️  No route to simulate.")
            return

        print("\n🚑 Emergency Vehicle Movement:")
        print("   Route:", " → ".join(self.route))
        print()

        for i, junction in enumerate(self.route):
            # Determine where the vehicle is going next
            if i < len(self.route) - 1:
                next_junction = self.route[i + 1]
                status = f"Moving to {next_junction}"
            else:
                status = "Destination reached ✅"

            signal_state = signals.get(junction, SIGNAL_NORMAL)
            print(f"  📍 Current: {junction}  |  Signal: {signal_state}  |  {status}")

        print()


# ── Route Display Helper ───────────────────────────────────────────────────

def format_route(route):
    """Return the route as a readable arrow-joined string, e.g. 'J1 → J2 → J4'."""
    if not route:
        return "No route"
    return " → ".join(route)
