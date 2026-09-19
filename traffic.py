import random


def generate_vehicles(junctions, min_vehicles=5, max_vehicles=30):
    traffic = {}

    for junction in junctions:
        traffic[junction] = random.randint(
            min_vehicles,
            max_vehicles
        )

    return traffic