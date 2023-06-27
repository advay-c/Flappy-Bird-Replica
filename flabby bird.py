import pygame
import os
import random

pygame.font.init()

WIDTH, HEIGHT = 609, 663 #sets the width and height of the window
BIRD_HEIGHT = 110
BIRD_WIDTH = 110
VEL = 5
PIPE_WIDTH = 100
pipe_vel = 6  # controls pipe and game speed
SCORE = 0

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

SKY = pygame.image.load(os.path.join('imgs', 'skyd.png'))
ground_image = pygame.image.load(os.path.join('imgs', 'sky_bottom.png'))
restart = pygame.image.load(os.path.join('imgs', 'restart.png'))
ground_width = ground_image.get_width()

def display_score():
    font = pygame.font.Font(os.path.join('imgs', 'font.otf'), 55)
    text = font.render(str(SCORE), True, (0, 0, 0))
    WINDOW.blit(text, (295, 90))

def update_score():
    global SCORE
    SCORE += 1  # increase score by one per second

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((ground_width * 2, ground_image.get_height()))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.image.blit(ground_image, (0, 0))
        self.image.blit(ground_image, (ground_width, 0))

    def update(self):
        self.rect.x -= pipe_vel
        if self.rect.x <= -ground_width:
            self.rect.x = 0

ground = Ground(0, HEIGHT - ground_image.get_height())

PIPE_TOP = pygame.image.load(os.path.join('imgs', 'pipe_top.png'))
PIPE_BOTTOM = pygame.image.load(os.path.join('imgs', 'pipe_bottom.png'))

BIRD = pygame.image.load(os.path.join('imgs', 'bird.png'))
BIRD = pygame.transform.scale(BIRD, (BIRD_WIDTH, BIRD_HEIGHT))

bird_x = WIDTH // 2 - BIRD_WIDTH // 2  # Initial x position of the bird
bird_y = HEIGHT // 2 - BIRD_HEIGHT // 2  # Initial y position of the bird

bird_movey = 0  # Vertical movement of the bird
bird_gravity = 0.4  # Normal gravity value
collision_gravity = 4  # Gravity value when collision occurs

pipe_x = WIDTH + PIPE_WIDTH  # Initial x position of the pipes
pipe_gap = 200  # Gap between the top and bottom pipes

def generate_pipe_height():
    min_height = 100
    max_height = HEIGHT - pipe_gap - min_height - BIRD_HEIGHT
    return random.randint(min_height, max_height)

pipe_height = generate_pipe_height()  # Random height for the pipes
pipe_y_bottom = pipe_height + pipe_gap  # Calculate the y position of the bottom pipe

def gravity():
    global bird_movey
    bird_movey += bird_gravity  # Increase the bird's vertical movement with gravity

def check_collision():
    bird_rect = BIRD.get_rect(topleft=(bird_x, bird_y))
    bird_mask = pygame.mask.from_surface(BIRD)

    pipe_top_rect = PIPE_TOP.get_rect(topleft=(pipe_x, pipe_height - PIPE_TOP.get_height()))
    pipe_bottom_rect = PIPE_BOTTOM.get_rect(topleft=(pipe_x, pipe_y_bottom))

    pipe_top_mask = pygame.mask.from_surface(PIPE_TOP)
    pipe_bottom_mask = pygame.mask.from_surface(PIPE_BOTTOM)

    offset_top = (pipe_x - bird_x, pipe_height - PIPE_TOP.get_height() - bird_y)
    offset_bottom = (pipe_x - bird_x, pipe_y_bottom - bird_y)

    collision_top = bird_mask.overlap(pipe_top_mask, offset_top)
    collision_bottom = bird_mask.overlap(pipe_bottom_mask, offset_bottom)

    return collision_top or collision_bottom

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, window):

        action = False

        pos = pygame.mouse.get_pos()

        #check if mouse is over button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
                
        window.blit(self.image, (self.rect.x, self.rect.y))

        return action

button = Button(WIDTH // 2 - 65, HEIGHT // 2 - 15, restart)

running = True
clock = pygame.time.Clock()
game_over = False
falling = True #makes seperate function for falling bird
bird_gravity = 0.4  # Gravity applied to the bird
collision_gravity = 8  # Gravity applied to the bird after collision
jump_velocity = -7  # Velocity applied when the bird jumps

def restart_game():
    global bird_y, bird_movey, pipe_x, pipe_height, pipe_y_bottom, SCORE, game_over, falling, pipe_vel
    bird_y = HEIGHT // 2 - BIRD_HEIGHT // 2
    bird_movey = 0
    pipe_x = WIDTH + PIPE_WIDTH
    pipe_height = generate_pipe_height()
    pipe_y_bottom = pipe_height + pipe_gap
    SCORE = 0
    game_over = False
    falling = True
    pipe_vel = 5

while running:
    clock.tick(60)  # makes frame rate 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys_pressed = pygame.key.get_pressed()  # Get the state of all keyboard keys

    if keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:  # Flap the bird
        if not game_over:
            bird_movey = jump_velocity

    if not game_over:
        if check_collision():
            falling = True
            bird_movey = collision_gravity  # Make the bird fall very fast after collision
            pipe_vel = 0  # Pause the pipe movement

        if falling:
            bird_movey += bird_gravity  # Apply gravity to the falling bird

        pipe_x -= pipe_vel 

        # If the pipe reaches the left side of the screen, reset its position
        if pipe_x < -PIPE_WIDTH:
            pipe_x = WIDTH
            pipe_height = generate_pipe_height()  # Random height for the pipes
            pipe_y_bottom = pipe_height + pipe_gap  # Calculate the y position of the bottom pipe
            update_score()  # Update the score when the pipe goes off-screen

        WINDOW.blit(SKY, (0, 0))  # Draw the sky background

        WINDOW.blit(PIPE_TOP, (pipe_x, pipe_height - PIPE_TOP.get_height()))  # Draw the top pipe
        WINDOW.blit(PIPE_BOTTOM, (pipe_x, pipe_y_bottom))  # Draw the bottom pipe

        ground.update()
        WINDOW.blit(ground.image, ground.rect)  # Draw the ground

        WINDOW.blit(BIRD, (bird_x, bird_y))  # Draw the bird at its updated position

        display_score()  # Display the score

        pygame.display.update()

        bird_y += bird_movey  # Update the bird's position with vertical movement

        # Ensure the bird stays within the screen bounds
        if bird_y < 0:  # Restrict going above y=0
            bird_y = 0
            bird_movey = 0
        elif bird_y > HEIGHT - BIRD_HEIGHT:  # Restrict going below y=height-BIRD_HEIGHT
            bird_y = HEIGHT - BIRD_HEIGHT
            bird_movey = 0
            if not game_over:
                game_over = True  # Set game over when the bird hits the ground

    if game_over:
        bird_movey = collision_gravity  # Make the bird fall very fast after hitting the ground
        pipe_vel = 0  # Pause the pipe movement

        if button.draw(WINDOW) == True:
            game_over = False

        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(mouse_pos):
            restart_game()

        bird_y += bird_movey  # Update the bird's position with vertical movement

        if bird_y >= HEIGHT - BIRD_HEIGHT:  # Check if the bird hits the ground again
            game_over_text = pygame.image.load(os.path.join('imgs', 'gameover.png'))
            WINDOW.blit(game_over_text, (200, 255))

    pygame.display.update()

pygame.quit()
