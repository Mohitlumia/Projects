import numpy as np

class Rope_element:
    def __init__(self, x, y):
        self.pos = np.array([x, y], dtype=float)
        self.old_pos = np.array([x, y], dtype=float)
        self.vx = 0
        self.vy = 0
        self.next = None
        self.prev = None