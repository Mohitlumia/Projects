import pygame
from objects.loop_rope import Loop_Rope

def main():

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Simulation Screen")
    clock = pygame.time.Clock()

    # Create a Loop_Rope instance
    loop_rope = Loop_Rope(400, 300, 100, 20)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Clear the screen with white
        loop_rope.update()
        loop_rope.draw(screen)
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()