import pygame
import math
import numpy as np

class Rope_element:
    def __init__(self, x, y):
        self.pos = np.array([x, y], dtype=float)
        self.vx = 0
        self.vy = 0
        self.next = None
        self.prev = None
        

class Loop_Rope:
    def __init__(self, centre_x, centre_y, radius, num_elements): 
        self.elements = []
        self.num_elements = num_elements
        angle_step = 2 * 3.14159 / num_elements
        for i in range(num_elements):
            angle = i * angle_step
            x = centre_x + radius * math.cos(angle)
            y = centre_y + radius * math.sin(angle)
            element = Rope_element(x, y)
            if self.elements:
                element.prev = self.elements[-1]
                self.elements[-1].next = element
            self.elements.append(element)
        # Link last to first to make it a loop
        self.elements[0].prev = self.elements[-1]
        self.elements[-1].next = self.elements[0]
    
    def update(self, iterations=50, circles=None):
        if circles is None:
            circles = []
        for _ in range(iterations):
            # distance constraints (closed loop)
            for i in range(self.num_elements):
                j = (i + 1) % self.num_elements
                n1 = self.elements[i]
                n2 = self.elements[j]
                d = n2.pos - n1.pos
                dist = np.linalg.norm(d)
                if dist == 0.0:
                    d = np.array([1e-6, 0.0])
                    dist = np.linalg.norm(d)
                diff = (dist - 15) / dist
                correction = 0.5 * diff * d
                n1.pos += correction
                n2.pos -= correction

    def draw(self, screen):
        for element in self.elements:
            #pygame.draw.circle(screen, (0, 0, 0), (int(element.pos[0]), int(element.pos[1])), 5)
            pygame.draw.circle(screen, (0, 0, 0), (element.pos[0], element.pos[1]), 5)
            if element.next:
                #pygame.draw.line(screen, (0, 0, 0), (int(element.pos[0]), int(element.pos[1])), (int(element.next.pos[0]), int(element.next.pos[1])), 2)
                pygame.draw.line(screen, (0, 0, 0), (element.pos[0], element.pos[1]), (element.next.pos[0], element.next.pos[1]), 2)
        