import pygame
from pygame.locals import * 

FPS = 60

def background_img(surface):
    # Load the background image
    bg = pygame.image.load(r"flappy birds/resources/flappy-bird-background-png-8.png")
    bg = pygame.transform.scale(bg, (surface.get_width(), surface.get_height()))

    surface.blit(bg, (0, 0))

if __name__ == "__main__":
    pygame.init()  

    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Flappy Bird")

    clock = pygame.time.Clock()

    running = True
    pause = False

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        # Draw the background image
        background_img(screen)

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(FPS)

    pygame.quit()
