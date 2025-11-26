import numpy as np
import pygame

class Circle_obstacle:
    def __init__(self, x, y, radius):
        self.pos = np.array([x, y], dtype=float)  
        self.radius = radius
        self.ignore_collision = False

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.pos[0], self.pos[1]), self.radius)