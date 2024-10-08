import numpy as np

class GlobalMap:
    def __init__(self):
        self.map = np.zeros((100, 100))

    def update(self, x, y):
        self.map[x, y] = 1

    def get_map(self):
        return self.map
    
class LocalMap:
    def __init__(self):
        self.map = np.zeros((10, 10))

    def update(self, x, y):
        self.map[x, y] = 1

    def get_map(self):
        return self.map