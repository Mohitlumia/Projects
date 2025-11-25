import pygame
import math

class Rope_element:
    def __init__(self, x, y, mass=1):
        self.x = x
        self.y = y
        self.next = None
        self.prev = None

class Loop_Rope:
    def __init__(self, centre_x, centre_y, radius, num_elements):
        self.elements = []
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
    
    def update(self):
        # Placeholder for update logic (e.g., physics simulation)
        pass

    def draw(self, screen):
        for element in self.elements:
            #pygame.draw.circle(screen, (0, 0, 0), (int(element.x), int(element.y)), 5)
            pygame.draw.circle(screen, (0, 0, 0), (element.x, element.y), 5)
            if element.next:
                #pygame.draw.line(screen, (0, 0, 0), (int(element.x), int(element.y)), (int(element.next.x), int(element.next.y)), 2)
                pygame.draw.line(screen, (0, 0, 0), (element.x, element.y), (element.next.x, element.next.y), 2)
        