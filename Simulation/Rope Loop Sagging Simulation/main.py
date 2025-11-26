import pygame
from objects.loop_rope import Loop_Rope
from objects.circle_obstacle import Circle_obstacle

def main():

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Simulation Screen")
    clock = pygame.time.Clock()

    # Create a Loop_Rope instance
    loop_rope = Loop_Rope(400, 300, 100, 50)

    # Create a CircleObstacle instance
    circle_obstacles = Circle_obstacle(400, 300, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Clear the screen with white
        loop_rope.apply_forces()
        loop_rope.update(circle=circle_obstacles)
        loop_rope.draw(screen)
        circle_obstacles.draw(screen)
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()