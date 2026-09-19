import networkx as nx
from typing import Dict, List, Any
import os
import pickle
import logging

logger = logging.getLogger(__name__)

class TrafficNetwork:
    """
    Manages the urban traffic network graph (intersections and roads).
    Uses NetworkX for representation and routing.
    """
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_intersection(self, id: str, x: float, y: float, **kwargs):
        """Adds an intersection (node) to the network."""
        self.graph.add_node(id, x=x, y=y, **kwargs)

    def add_road(self, u: str, v: str, length: float, capacity: int, speed_limit: float, lanes: int = 1, **kwargs):
        """Adds a road (directed edge) between two intersections."""
        self.graph.add_edge(
            u, v,
            length=length,
            capacity=capacity,
            speed_limit=speed_limit,
            lanes=lanes,
            weight=length / speed_limit if speed_limit > 0 else float('inf'), # Basic travel time
            **kwargs
        )

    def get_shortest_path(self, source: str, target: str, weight: str = 'weight') -> List[str]:
        """Calculates the shortest path between two intersections."""
        try:
            return nx.shortest_path(self.graph, source=source, target=target, weight=weight)
        except nx.NetworkXNoPath:
            return []
        except nx.NodeNotFound:
            return []

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the graph for API responses."""
        nodes = [{"id": n, **d} for n, d in self.graph.nodes(data=True)]
        edges = [{"source": u, "target": v, **d} for u, v, d in self.graph.edges(data=True)]
        return {"nodes": nodes, "edges": edges}

    @classmethod
    def create_default_network(cls) -> 'TrafficNetwork':
        """Creates the default 6-intersection demonstration network."""
        net = cls()
        
        # Intersections
        net.add_intersection("I1", x=0, y=100, name="North West")
        net.add_intersection("I2", x=100, y=100, name="North Center")
        net.add_intersection("I3", x=200, y=100, name="North East")
        net.add_intersection("I4", x=0, y=0, name="South West")
        net.add_intersection("I5", x=100, y=0, name="South Center")
        net.add_intersection("I6", x=200, y=0, name="South East")

        # Horizontal Roads (bi-directional as two directed edges)
        for u, v in [("I1", "I2"), ("I2", "I3"), ("I4", "I5"), ("I5", "I6")]:
            net.add_road(u, v, length=100, capacity=20, speed_limit=15)
            net.add_road(v, u, length=100, capacity=20, speed_limit=15)

        # Vertical Roads
        for u, v in [("I1", "I4"), ("I2", "I5"), ("I3", "I6")]:
            net.add_road(u, v, length=100, capacity=15, speed_limit=10)
            net.add_road(v, u, length=100, capacity=15, speed_limit=10)

        return net
    
    @classmethod
    def load_osmnx_network(cls, place_name: str) -> 'TrafficNetwork':
        """Loads a real road network using osmnx."""
        import osmnx as ox
        
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
        os.makedirs(data_dir, exist_ok=True)
        cache_path = os.path.join(data_dir, f"{place_name.replace(' ', '_').replace(',', '')}.pkl")
        
        if os.path.exists(cache_path):
            logger.info(f"Loading cached OSMnx network for '{place_name}' from {cache_path}")
            try:
                with open(cache_path, "rb") as f:
                    return pickle.load(f)
            except Exception as e:
                logger.error(f"Failed to load cache: {e}. Will re-download.")

        logger.info(f"Downloading OSMnx network for '{place_name}' (this requires internet)...")
        G = ox.graph_from_place(place_name, network_type='drive')
        
        net = cls()
        for node, data in G.nodes(data=True):
            net.add_intersection(str(node), x=data['x'], y=data['y'], name=str(node))
            
        for u, v, key, data in G.edges(keys=True, data=True):
            length = data.get('length', 100)
            # handle lists for maxspeed or speed limits
            speed_limit = data.get('maxspeed', 15)
            if isinstance(speed_limit, list):
                speed_limit = speed_limit[0]
            try:
                if isinstance(speed_limit, str):
                    speed_limit = float(speed_limit.split(' ')[0])
            except:
                speed_limit = 15
            
            lanes = data.get('lanes', 1)
            if isinstance(lanes, list):
                lanes = lanes[0]
            try:
                lanes = int(lanes)
            except:
                lanes = 1
                
            capacity = lanes * 20
                
            net.add_road(str(u), str(v), length=float(length), capacity=capacity, speed_limit=float(speed_limit), lanes=lanes)

        with open(cache_path, "wb") as f:
            pickle.dump(net, f)
            
        logger.info(f"Successfully loaded and cached OSMnx network with {len(net.graph.nodes)} nodes and {len(net.graph.edges)} edges.")
        return net

def initialize_network():
    place = os.getenv("NETWORK_PLACE", "Piedmont, California, USA")
    try:
        net = TrafficNetwork.load_osmnx_network(place)
        print(f"USING OSMNX NETWORK for {place}")
        return net
    except Exception as e:
        print(f"FAILED to load OSMnx network: {e}. FALLING BACK to grid network.")
        return TrafficNetwork.create_default_network()

# Global instance for now
default_network = initialize_network()
