from collections import defaultdict

class Frame:
    def __init__(self, frame_id, instance_list):
        self.frame_id = frame_id
        self.instance_list = instance_list

    def to_export_format(self):
        instances = []
        for instance in self.instance_list:
            instances.append(instance.to_export_format())

        return (self.frame_id, instances)
