import numpy as np

def convert_points(packet_map):
    points_map = { }

    for frame in packet_map.keys():
        points = []
        for point in packet_map[frame][0]['points']:
            points.append([point['x'], point['y']])

        points_map[frame] = np.array(points)

    return points_map

def flip_coordinates(points, img):
    height = img.shape[0]
    for i in range(len(points)):
        points[i][1] = height - points[i][1]

    return points
