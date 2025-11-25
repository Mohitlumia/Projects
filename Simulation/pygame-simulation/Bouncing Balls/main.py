import pygame
from objects.circles import Circles
import random


def main():

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Simulation Screen")
    clock = pygame.time.Clock()

    width, height = 800, 600
    Circles.width = width
    Circles.height = height

    circles_lis = []
    for _ in range(50): # Create 50 circles with random attributes
        r = random.randint(10, 30)
        x = random.randint(r, width - r)
        y = random.randint(r, height - r)
        vx = random.uniform(-4, 4)
        vy = random.uniform(-4, 4)
        color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

        circles_lis.append(Circles(x, y, r, color, vx, vy))


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Clear the screen with white
        for circle in circles_lis:    # Draw and update each circle
            circle.update()
            circle.draw(screen)
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()