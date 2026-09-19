def traffic_surge(traffic, junction, multiplier=3):
    traffic[junction] *= multiplier
    return traffic


def road_closure(road_network, road):
    if road_network.has_edge(*road):
        road_network.remove_edge(*road)

    return road_network