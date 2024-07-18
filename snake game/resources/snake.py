import pygame
from pygame.locals import * #here are the imports we used, the pygame one is to use pygame's own libraries. OS is so we can easily use files, see as i put r infront of the path
import time
import os
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple: # Apple class, key thing for each object you make in these things.
    def __init__(self, parent_screen): # Initializing the apple with with this constructor, we will load the image with the the imported pygame modules, also intializing the parent screen
        self.image = pygame.image.load(r"snake game\resources\apple.jpg").convert()
        self.parent_screen = parent_screen # this refers to the main screen (surface) in the Game class
        self.x = SIZE * 3   # here we are just setting the position of the apple
        self.y = SIZE * 3
    
    def draw(self): #This constructor draws the apple to that position and updates the display, Blit and flip are the pygame function to do that.
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self): # this comstructor moves the apple's placement to random places 
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 19) * SIZE

class Snake: #Next object is the snake, so we make a class
    def __init__(self, parent_screen, length): # in this initializing constructor, which we will need for all of the, we add a new parameter length which controls size of the snake.
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load(r"snake game/resources/block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'down' # this we initializing that the snake goes down when we start the game.

    def increase_length(self): # using this to increase the size of the snake
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    # next couple lines are the directions of the snake
    def move_left(self):
        if self.direction != 'right':
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'

    def draw(self): # this is a snake draw function, we had to use a loop so we can be able to add blocks, as we eat apples
        for i in range(self.length): # for however long the length is...
            self.parent_screen.blit(self.block, (self.x[i], self.y[i])) #... create a block
        pygame.display.flip() # add to the screen

    def walk(self): # NOw in this walk we are essentially updating the previous block to become the now initial block
        # Update the positions of all segments except the head
        # Starting from the tail and moving towards the head
        for i in range(self.length - 1, 0, -1):
        # Set the position of the current segment to the position of the previous segment
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # Update the head position based on the current direction
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw() # call the draw function at the end 

class Game: # game class is the where we run everything and anything non specific
    def __init__(self): # in the initializing contructor we initialize pygame, then we set the screen size
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 1000)) # we can shange the screen size as we want
        self.surface.fill((110, 110, 5)) # this is the screen color, change this shi too
        pygame.mixer.init()
        self.play_backgroundMusic()
        
        self.snake = Snake(self.surface, 1) # here we create a snake object, and we draw it on to the game's surface
        self.snake.draw()
        self.apple = Apple(self.surface) # we do the same with the apple
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2): # this is the collision mechanism, still a little too unsure about this
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
            
        return False
    
    def render_bg_image(self):
        bg = pygame.image.load(r"snake game\resources\background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self): # we also create a play constructor which call for the snake to walk and for the apple to display on the screen
        self.render_bg_image()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y): # here we are saying once the snake collides with the apple it increases it's length and the apple moves to a random spot
            sound = pygame.mixer.Sound(r"snake game/resources/1_snake_game_resources_ding.mp3")
            pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.apple.move()

        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound = pygame.mixer.Sound(r"snake game\resources\crash.mp3")
                pygame.mixer.Sound.play(sound)
                raise "Game over"
            
    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game Over! yor Score is: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(f"Press ESC to play again!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def play_backgroundMusic(self):
        pygame.mixer.music.load(r"snake game\resources\bg_music_1.mp3")
        pygame.mixer.music.play()


    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def display_score(self): # this is how we display the score
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def run(self): #this is the run function where we have a game running loop, we honestly could use this code anywhere       
        running = True

        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    if event.key == K_LEFT:
                        self.snake.move_left()

            try: 
                if not pause:       
                    self.play() # we call the play function after the loop so it can all work together, and save some space too!
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            
            time.sleep(0.2) # we use time so the snake keeps moving even after we press the button direction

        pygame.quit()

# Main function 
if __name__ == "__main__":
    game = Game()
    game.run()

    # its actually crazy, we create a game object so we can call it in the main function, game.run() which is the game loop and then the play function, which has the walk and draw constructors from the snake and apple classes, so it's important to use classes and functions

