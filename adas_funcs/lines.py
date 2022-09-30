import math
import numpy as np
from numpy.linalg import norm

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

def get_pairs(lines, height):
    pos, neg = get_groups(sorted(lines, key = lambda x: x[4]))
    pairs = get_pairs_by_group(unite_lines(pos, height))
    pairs += get_pairs_by_group(unite_lines(neg, height))
    return pairs

def get_pairs_by_group(group, intersection_perc_threshold = 0.65):
    pairs = []
    block = set()
    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            if i in block or j in block:
                continue

            if 10 < min_dist_between_lines(group[i], group[j]) < 20:
                perc = intersection_perc(group[i], group[j])
                if perc > intersection_perc_threshold:
                    pairs.append([group[i], group[j]])
                    block.add(i)
                    block.add(j)

    return pairs

#деление линий на группы относительно положения автомобиля (слева, справа)
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

#
def get_polygons(lines, height):
    pairs = get_pairs(lines, height)

    polygons = []
    for pair in pairs:
        points = []
        for line in pair:
            points.append([line[0], line[1]])
            points.append([line[2], line[3]])

        points = sort_points(points)

        polygons.append(np.array(points, np.int32))

    return polygons

#сортировка вершин четырехугольника для получения выпуклого многоугольника
def sort_points(points):
    points.sort(key = lambda x: x[1], reverse=True)

    a = [points[0][0], points[0][1], points[2][0], points[2][1], None, None]
    b = [points[1][0], points[1][1], points[3][0], points[3][1], None, None]
    if not check_intersection(a, b):
        points[1], points[0] = points[0], points[1]
    return points


def unite_lines(lines, height):
    flag = True

    while flag:
        temp = []
        block = set()
        flag = False
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                if (i in block) or (j in block):
                    continue

                a = lines[i]
                b = lines[j]
                perc = intersection_perc(a, b)
                if perc < 0.01:
                    continue

                a_x1, a_y1, a_x2, a_y2, a_x, a_k = a
                b_x1, b_y1, b_x2, b_y2, b_x, b_k = b

                if abs(a_k) < abs(b_k * 0.98) or abs(b_k * 1.02) < abs(a_k):
                    continue

                if min_dist_between_lines(a, b) > 3:
                    continue

                flag = True
                block.add(i)
                block.add(j)
                pts = sorted([[a_x1, a_y1], [a_x2, a_y2], [b_x1, b_y1], [b_x2, b_y2]], key = lambda x: x[1])
                c_x1 = pts[0][0]
                c_y1 = pts[0][1]
                c_x2 = pts[3][0]
                c_y2 = pts[3][1]
                temp.append([c_x1, c_y1, c_x2, c_y2, get_k([[c_x1, c_y1, c_x2, c_y2]]), get_x([[c_x1, c_y1, c_x2, c_y2]], height)])

        for i in range(len(lines)):
            if i in block:
                continue

            temp.append(lines[i])

        lines = temp.copy()

    return lines

#расстояние между отрезком и точкой
def distance_between_point_and_lines(line, point):
    p1, p2 = line
    p1 = np.asarray(p1)
    p2 = np.asarray(p2)
    point = np.asarray(point)
    d = norm(np.cross(p2 - p1, p1 - point)) / norm(p2 - p1)

    return d

#подсчет минимального расстояния между парой отрезков
def min_dist_between_lines(a, b):
    is_intersect = check_intersection(a, b)
    if is_intersect:
        return 0

    a_x1, a_y1, a_x2, a_y2, a_x, a_k = a
    b_x1, b_y1, b_x2, b_y2, b_x, b_k = b

    dist = min([
        distance_between_point_and_lines([[a_x1, a_y1], [a_x2, a_y2]], [b_x1, b_y1]),
        distance_between_point_and_lines([[a_x1, a_y1], [a_x2, a_y2]], [b_x2, b_y2]),
        distance_between_point_and_lines([[b_x1, b_y1], [b_x2, b_y2]], [a_x1, a_y1]),
        distance_between_point_and_lines([[b_x1, b_y1], [b_x2, b_y2]], [a_x2, a_y2])
    ])

    return dist

#проверка пересекаются ли отрезки a, b
def check_intersection(a, b):
    # y = kx + c
    a_x1, a_y1, a_x2, a_y2, _, a_k = a
    b_x1, b_y1, b_x2, b_y2, _, b_k = b

    if not a_k:
        a_k = get_k([[a_x1, a_y1, a_x2, a_y2]])
    if not b_k:
        b_k = get_k([[b_x1, b_y1, b_x2, b_y2]])

    if a_k == b_k:
        return False

    I = [max( min(a_x1, a_x2), min(b_x1, b_x2) ),
          min( max(a_x1, a_x2), max(b_x1, b_x2) )]

    a_c = a_y1 - a_k * a_x1
    b_c = b_y1 - b_k * b_x1

    root = (a_c - b_c) / (b_k - a_k)

    return I[0] < root < I[1]
