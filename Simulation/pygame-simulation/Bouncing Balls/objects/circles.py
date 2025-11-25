import pygame

class Circles():

    width = 800
    height = 600

    def __init__(self, x, y, radius, color, vx, vy):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx = vx
        self.vy = vy

    def update(self):
        # Update position
        self.x += self.vx
        self.y += self.vy

        # Bounce from walls
        if self.x - self.radius < 0 or self.x + self.radius > self.width:
            self.vx = -self.vx

        if self.y - self.radius < 0 or self.y + self.radius > self.height:
            self.vy = -self.vy

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
