import time
import uuid
import asyncio
import os
from typing import Dict, Any, List
from app.simulation.network import default_network

class Vehicle:
    def __init__(self, start_node: str, end_node: str, route: list):
        self.id = str(uuid.uuid4())[:8]
        self.start_node = start_node
        self.end_node = end_node
        self.route = route
        self.current_edge_index = 0
        self.progress = 0.0 # 0.0 to 1.0 along the current edge
        self.waiting_time = 0.0
        self.status = "moving" # moving, waiting

class TrafficSignal:
    def __init__(self, node_id: str, incoming_edges: List[str]):
        self.node_id = node_id
        self.incoming_edges = incoming_edges
        self.current_green_edge = incoming_edges[0] if incoming_edges else None
        self.time_since_last_change = 0.0
        self.fixed_green_duration = 10.0 # seconds

    def update(self, dt: float):
        self.time_since_last_change += dt

class ClassicalOptimizer:
    def __init__(self, simulator, mode="fixed"):
        self.simulator = simulator
        self.mode = mode # "fixed" or "rule_based"

    def optimize(self):
        for node_id, signal in self.simulator.signals.items():
            if not signal.incoming_edges:
                continue
            
            if self.mode == "fixed":
                if signal.time_since_last_change >= signal.fixed_green_duration:
                    # Switch to next edge
                    current_idx = signal.incoming_edges.index(signal.current_green_edge)
                    next_idx = (current_idx + 1) % len(signal.incoming_edges)
                    signal.current_green_edge = signal.incoming_edges[next_idx]
                    signal.time_since_last_change = 0.0
            
            elif self.mode == "rule_based":
                # Find the edge with the longest queue
                queues = {edge: 0 for edge in signal.incoming_edges}
                for v in self.simulator.vehicles.values():
                    if v.status == "waiting" and v.current_edge_index < len(v.route) - 1:
                        current_u = v.route[v.current_edge_index]
                        if v.route[v.current_edge_index + 1] == node_id:
                            # Vehicle is waiting on incoming edge `current_u`
                            queues[current_u] += 1
                
                max_queue_edge = max(queues, key=queues.get)
                # If current green has no queue and another has queue, switch immediately
                # Otherwise, enforce min/max green times
                min_green = 5.0
                max_green = 20.0
                if signal.time_since_last_change >= min_green:
                    if queues[max_queue_edge] > 0 and max_queue_edge != signal.current_green_edge:
                        signal.current_green_edge = max_queue_edge
                        signal.time_since_last_change = 0.0
                    elif signal.time_since_last_change >= max_green:
                        # Force cycle if max green reached
                        current_idx = signal.incoming_edges.index(signal.current_green_edge)
                        next_idx = (current_idx + 1) % len(signal.incoming_edges)
                        signal.current_green_edge = signal.incoming_edges[next_idx]
                        signal.time_since_last_change = 0.0

class CustomTrafficSimulator:
    def __init__(self, network=default_network):
        self.network = network
        self.vehicles: Dict[str, Vehicle] = {}
        self.signals: Dict[str, TrafficSignal] = {}
        self.running = False
        self.time_step = 1.0 # seconds per tick
        self.current_time = 0.0
        
        # Metrics
        self.total_wait_time = 0.0
        self.throughput = 0
        
        self.optimizer = ClassicalOptimizer(self, mode="rule_based")
        self._init_signals()
        
    def reset(self):
        self.vehicles.clear()
        self.current_time = 0.0
        self.total_wait_time = 0.0
        self.throughput = 0
        self._init_signals()
        
    def apply_scenario(self, scenario_type: str, edge_id: str = None, demand_level: str = None):
        if scenario_type == "accident":
            pass # simplified
        elif scenario_type == "road_closure":
            pass # simplified
        elif scenario_type == "rush_hour":
            pass # simplified

    async def run_loop(self):
        tick_ms = int(os.getenv("SIM_TICK_MS", "1000"))
        tick_s = tick_ms / 1000.0
        while True:
            if self.running:
                self.tick()
            await asyncio.sleep(tick_s)

    def _init_signals(self):
        for node in self.network.graph.nodes:
            incoming = [u for u, v in self.network.graph.edges if v == node]
            if incoming:
                self.signals[node] = TrafficSignal(node, incoming)

    def add_vehicle(self, start: str, end: str):
        route = self.network.get_shortest_path(start, end)
        if len(route) > 1:
            v = Vehicle(start, end, route)
            self.vehicles[v.id] = v
            return v
        return None

    def tick(self):
        """Advances the simulation by one time step."""
        if not self.running:
            return

        self.current_time += self.time_step
        
        # Run optimization
        self.optimizer.optimize()
        
        # Update signals
        for sig in self.signals.values():
            sig.update(self.time_step)

        # Update vehicles
        for v in list(self.vehicles.values()):
            if v.current_edge_index >= len(v.route) - 1:
                # Reached destination
                self.throughput += 1
                del self.vehicles[v.id]
                continue

            current_u = v.route[v.current_edge_index]
            current_v = v.route[v.current_edge_index + 1]
            
            # If vehicle is at the end of an edge, check signal
            if v.progress >= 1.0:
                signal = self.signals.get(current_v)
                if signal and signal.current_green_edge != current_u:
                    # Red light, must wait
                    v.status = "waiting"
                    v.waiting_time += self.time_step
                    self.total_wait_time += self.time_step
                    continue
                else:
                    # Green light, enter intersection
                    v.status = "moving"
                    v.current_edge_index += 1
                    v.progress = 0.0
                    continue # process movement in next tick

            # Normal movement
            v.status = "moving"
            edge_data = self.network.graph.get_edge_data(current_u, current_v)
            distance = edge_data['speed_limit'] * self.time_step
            progress_increment = distance / edge_data['length']
            
            v.progress = min(1.0, v.progress + progress_increment)

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

# Global instance for now
simulator_engine = CustomTrafficSimulator()
