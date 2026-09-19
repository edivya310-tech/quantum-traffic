import networkx as nx


def create_network():
    road_network = nx.Graph()

    # Add junctions
    road_network.add_nodes_from(["J1", "J2", "J3", "J4"])

    # Add roads
    road_network.add_edges_from([
        ("J1", "J2"),
        ("J1", "J3"),
        ("J2", "J4"),
        ("J3", "J4")
    ])

    return road_network