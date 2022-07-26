def select_lines(lines, width, height):
    marking = []

    for line in lines:
        k = get_k(line)
        x = get_x(line, height)
        if (0.5 < abs(k) < 1.3) and (900 < x < 1200):
            marking.append(line[0])

    return marking

def get_k(line):
    x1, y1, x2, y2 = line[0]
    k = (y2 - y1) / (x2 - x1)
    return k

def get_x(line, height):
    x1, y1, x2, y2 = line[0]
    x = (x1 / (x2 - x1) + (height - y1) / (y2 - y1)) * (x2 - x1)
    return x
