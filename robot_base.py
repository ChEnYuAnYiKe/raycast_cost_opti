import numpy as np
from map_world import GlobalMap, LocalMap

class RobotBase:
    def __init__(self):
        self.position = np.zeros(2)
        self.global_map = None
        self.local_map = None

    def set_position(self, x, y):
        self.position = np.array([x, y])

    def set_map(self, global_map, local_map):
        self.global_map = global_map
        self.local_map = local_map

    def move(self, x, y):
        self.position += np.array([x, y])
        self.global_map.update(*self.position)
        self.local_map.update(*self.position)

    def get_position(self):
        return self.position

    def get_global_map(self):
        return self.global_map.get_map()

    def get_local_map(self):
        return self.local_map.get_map()