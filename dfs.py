import pygame
from pygame.locals import *
import random

# Constants
FPS = 60
BACKGROUND_SPEED = 2
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

class Bird:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = 0
        
    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        
    def jump(self):
        self.velocity = JUMP_STRENGTH
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class ScrollingBackground:
    def __init__(self, image_path, surface):
        self.surface = surface
        self.background = pygame.image.load(image_path)
        self.background = pygame.transform.scale(self.background, (surface.get_width(), surface.get_height()))
        self.background_x = 0

    def update(self):
        # Move background to the left
        self.background_x -= BACKGROUND_SPEED
        # Reset background position if it goes off screen
        if self.background_x <= -self.surface.get_width():
            self.background_x = 0

    def draw(self):
        # Draw background image
        self.surface.blit(self.background, (self.background_x, 0))
        # Draw the second part of the background image
        self.surface.blit(self.background, (self.background_x + self.surface.get_width(), 0))

class Pipe:
    def __init__(self, x, gap_y):
        self.x = x
        self.gap_y = gap_y
        self.top_rect = pygame.Rect(x, 0, PIPE_WIDTH, gap_y)
        self.bottom_rect = pygame.Rect(x, gap_y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - (gap_y + PIPE_GAP))
        
    def update(self):
        self.x -= BACKGROUND_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        
    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.top_rect)
        pygame.draw.rect(surface, (0, 255, 0), self.bottom_rect)

    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0

    def collides_with(self, bird):
        return self.top_rect.colliderect(bird.rect) or self.bottom_rect.colliderect(bird.rect)

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")

    clock = pygame.time.Clock()

    # Initialize the scrolling background
    bg = ScrollingBackground(r"flappy birds/resources/flappy-bird-background-png-8.png", screen)
    bird = Bird(r"flappy birds/resources/Flappy-Bird-PNG-Photo.png", 100, SCREEN_HEIGHT // 2)

    pipes = []
    last_pipe = pygame.time.get_ticks()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_SPACE:
                    bird.jump()

        # Update background position
        bg.update()
        
        # Update bird position
        bird.update()

        # Generate new pipes
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > PIPE_FREQUENCY:
            gap_y = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
            pipes.append(Pipe(SCREEN_WIDTH, gap_y))
            last_pipe = current_time

        # Update pipes
        for pipe in pipes:
            pipe.update()

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if not pipe.is_off_screen()]

        # Check for collisions
        for pipe in pipes:
            if pipe.collides_with(bird):
                running = False

        # Draw everything
        bg.draw()
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(FPS)

    pygame.quit()
