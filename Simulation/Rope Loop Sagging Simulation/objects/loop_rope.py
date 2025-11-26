import pygame
import math
import numpy as np

from objects.rope_element import Rope_element
from objects.circle_obstacle import Circle_obstacle

class Loop_Rope:
    def __init__(self, centre_x, centre_y, radius, num_elements): 
        self.elements = []
        self.num_elements = num_elements
        angle_step = 2 * 3.14159 / num_elements
        self.step_length = 2 * radius * math.sin(angle_step / 2)
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
    

    def apply_forces(self, g=9.81, dt=0.1, damping=0.99):
        # Verlet integration in mm units
        for roop_element in self.elements:
            vel = (roop_element.pos - roop_element.old_pos) * damping
            roop_element.old_pos = roop_element.pos.copy()
            roop_element.pos = roop_element.pos + vel + np.array([0.0, g]) * (dt * dt)


    def update(self, iterations=50, circle=None):
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
                diff = (dist - self.step_length) / dist
                correction = 0.5 * diff * d
                n1.pos += correction
                n2.pos -= correction
            # collision with circle
            if circle and not circle.ignore_collision:
                for element in self.elements:
                    d = element.pos - circle.pos
                    dist = np.linalg.norm(d)
                    if dist < circle.radius + 5:  # 5 is the rope element radius
                        if dist == 0.0:
                            d = np.array([1e-6, 0.0])
                            dist = np.linalg.norm(d)
                        overlap = circle.radius + 5 - dist
                        correction = (overlap / dist) * d
                        element.pos += correction

    def draw(self, screen):
        for element in self.elements:
            pygame.draw.circle(screen, (0, 0, 0), (element.pos[0], element.pos[1]), 5)
            if element.next:
                pygame.draw.line(screen, (0, 0, 0), (element.pos[0], element.pos[1]), (element.next.pos[0], element.next.pos[1]), 2)
        