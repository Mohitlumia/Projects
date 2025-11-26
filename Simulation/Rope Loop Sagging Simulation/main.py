import pygame
from objects.loop_rope import Loop_Rope

def main():

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Simulation Screen")
    clock = pygame.time.Clock()

    # Create a Loop_Rope instance
    loop_rope = Loop_Rope(400, 300, 100, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for roop_element in loop_rope.elements:
            if roop_element.pos[1] > 600:
                roop_element.vy *= -0.7  # simple bounce effect
                roop_element.pos[1] = 600
            roop_element.vy += 0.1*9.81  # gravity
            roop_element.pos[0] += roop_element.vx
            roop_element.pos[1] += roop_element.vy

        screen.fill((255, 255, 255))  # Clear the screen with white
        loop_rope.update()
        loop_rope.draw(screen)
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()