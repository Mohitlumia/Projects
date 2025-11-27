import pygame
import numpy as np

class Circles():

    width = 500
    height = 500
    friction = 0
    restitution = 1


    def __init__(self, x, y, radius, color, vx, vy):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx = vx
        self.vy = vy
        self.colided = False

    def update(self, otherCircle=None):
        # Update position
        self.x += self.vx
        self.y += self.vy

        self.collide_wall()
        if otherCircle is not None:
            self.collide_otherCircle(otherCircle)


    def collide_wall(self):
        # Bounce from walls
        if (self.x - self.radius < 0 and self.vx < 0) or (self.x + self.radius > self.width and self.vx > 0):
            self.vx = -self.vx

        if (self.y - self.radius < 0 and self.vy < 0) or (self.y + self.radius > self.height and self.vy > 0):
            self.vy = -self.vy

    def collide_otherCircle(self, otherCircle=None):
        
        distance = np.linalg.norm(np.array([self.x, self.y]) - np.array([otherCircle.x, otherCircle.y]))
        if distance > self.radius + otherCircle.radius:
            return  # No collision
        if distance == 0:
            return
        normalX = (self.x - otherCircle.x)/ distance
        normalY = (self.y - otherCircle.y)/ distance

        relativeSpeedAlongNormal = np.dot(np.array([self.vx - otherCircle.vx, self.vy - otherCircle.vy]), np.array([normalX, normalY]))
        relativeSpeedAlongTangent = np.dot(np.array([self.vx - otherCircle.vx, self.vy - otherCircle.vy]), np.array([normalY, -normalX]))

        forceX = relativeSpeedAlongTangent/2 * normalY * self.friction
        forceY = relativeSpeedAlongTangent/2 * (-normalX) * self.friction
        
        # Elastic or inelastic collision response
        forceX += relativeSpeedAlongNormal/2 * normalX * (1 + self.restitution)
        forceY += relativeSpeedAlongNormal/2 * normalY * (1 + self.restitution)
        
        # Positional correction to avoid sinking
        penetration = (self.radius + otherCircle.radius) - distance
        self.x += penetration * normalX / 2
        self.y += penetration * normalY / 2
        otherCircle.x -= penetration * normalX / 2
        otherCircle.y -= penetration * normalY / 2

        self.vx -= forceX
        self.vy -= forceY
        otherCircle.vx += forceX    
        otherCircle.vy += forceY


    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
