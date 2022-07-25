import numpy as np

def convert_points(packet_map):
    points_map = { }

    for frame in packet_map.keys():
        points = []
        for point in packet_map[frame][0]['points']:
            points.append([point['x'], point['y']])

        points_map[frame] = np.array(points)

    return points_map
