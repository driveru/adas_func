import math
import numpy as np

def select_lines(lines, width, height):
    marking = []

    for line in lines:
        k = get_k(line)
        x = get_x(line, height)
        x_half = get_x(line, height / 2)
        if (0.5 < abs(k) < 1.3) and (900 < x < 1200):
            x1, y1, x2, y2 = line[0]
            marking.append([x1, y1, x2, y2, x_half, k])

    return marking

def get_k(line):
    x1, y1, x2, y2 = line[0]
    k = (y2 - y1) / (x2 - x1)
    return k

def get_x(line, height):
    x1, y1, x2, y2 = line[0]
    x = (x1 / (x2 - x1) + (height - y1) / (y2 - y1)) * (x2 - x1)
    return x

def intersection_perc(a, b):
    _, a_y1, _, a_y2, _, _ = a
    _, b_y1, _, b_y2, _, _ = b

    if a_y1 < a_y2:
        a_y1, a_y2 = a_y2, a_y1
    if b_y1 < b_y2:
        b_y1, b_y2 = b_y2, b_y1

    c_y1, c_y2 = [0, 0]
    if b_y2 < a_y1 < b_y1:
        c_y1 = a_y1
        if a_y2 < b_y2:
            c_y2 = b_y2
        else:
            c_y2 = a_y2
    elif a_y1 > b_y1:
        c_y1 = b_y1
        if b_y2 < a_y2 < b_y1:
            c_y2 = a_y2
        elif a_y2 < b_y2:
            c_y2 = b_y2
    if c_y1 * c_y2 == 0:
        return 0
    else:
        return max([0, min([(c_y1 - c_y2) / (a_y1 - a_y2), (c_y1 - c_y2) / (b_y1 - b_y2)])])

def get_pairs(lines):
    pos, neg = get_groups(sorted(lines, key = lambda x: x[4]))
    pairs = get_pairs_by_group(pos)
    pairs += get_pairs_by_group(neg)
    return pairs

def get_pairs_by_group(group, intersection_perc_threshold = 0.8):
    pairs = []
    block = set()
    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            if i in block or j in block:
                continue

            if 20 < abs(group[i][4] - group[j][4]) < 40:
                perc = intersection_perc(group[i], group[j])
                if perc > intersection_perc_threshold:
                    pairs.append([group[i], group[j]])
                    block.add(i)
                    block.add(j)

    return pairs

def get_groups(lines):
    pos = []
    neg = []
    for line in lines: # line = [x1, y1, x2, y2, x, k]
        _, _, _, _, _, k = line
        if k > 0:
            pos.append(line)
        else:
            neg.append(line)

    return (pos, neg)

def get_polygons(lines):
    pairs = get_pairs(lines)

    polygons = []
    for pair in pairs:
        points = []
        for line in pair:
            points.append([line[0], line[1]])
            points.append([line[2], line[3]])

        points = sort_points(points)

        polygons.append(np.array([points], np.int32))

    return polygons

def sort_points(points):
    points.sort(key = lambda x: x[1])
    if points[0][0] < points[1][0]:
        points[0], points[1] = points[1], points[0]
    if points[3][0] < points[2][0]:
        points[2], points[3] = points[3], points[2]

    return points
