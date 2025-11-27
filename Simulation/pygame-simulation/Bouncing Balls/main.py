import pygame
from objects.circles import Circles
from functions.random_circles import random_circles


def main():

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Simulation Screen")
    clock = pygame.time.Clock()

    width, height = 800, 600
    Circles.width = width
    Circles.height = height

    # Generate random circles
    circles = random_circles(10, width, height)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Clear the screen with white
        for i in range(len(circles)):  # Check collisions between circles
            circles[i].update()
            circles[i].draw(screen)
            for j in range(i+1, len(circles)):
                # Draw and update each circle
                circles[i].update(circles[j])
                circles[j].update()
        pygame.display.flip()
        clock.tick(120)  # Limit to 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()