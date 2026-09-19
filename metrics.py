def calculate_queue(vehicle_count, green_time):
    capacity = green_time * 2

    queue = max(0, vehicle_count - capacity)

    return queue


def calculate_waiting_time(queue):
    return queue * 2


def calculate_throughput(vehicle_count, queue):
    return max(0, vehicle_count - queue)