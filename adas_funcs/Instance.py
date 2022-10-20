class Instance:
    def __init__(self, polygon, name, frame_number):
        self.points = polygon
        self.name = name
        self.frame_number = frame_number

    def to_export_format(self):
        inst = {
        "name" : self.name,
        "frame_number" : self.frame_number,
        "type" : "polygon",  # or (point, line)
        "points" : []
        }

        def format_point(point):
            return {'x' : int(point[0]), 'y' : int(point[1])}

        for point in self.points:
            inst["points"].append(format_point(point))

        return inst
