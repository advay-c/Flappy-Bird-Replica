import pygame
import os
import random
pygame.font.init()

WIDTH, HEIGHT = 609, 663
BIRD_HEIGHT = 110
BIRD_WIDTH = 110
VEL = 5
PIPE_WIDTH = 100
pipe_vel = 7  # Adjust this value to control the pipe movement speed
SCORE = 0

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

SKY = pygame.image.load(os.path.join('imgs', 'skyd.png'))
ground_image = pygame.image.load(os.path.join('imgs', 'sky_bottom.png'))
ground_width = ground_image.get_width()

def display_score():
    font = pygame.font.SysFont('Inter', 40)
    text = font.render("Score: " + str(SCORE), True, (255, 255, 255))
    WINDOW.blit(text, (10, 10))

def update_score():
    global SCORE
    SCORE += 1

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
    bird_movey += 0.2  # Increase the bird's vertical movement
    
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)  # Limit the frame rate to 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys_pressed = pygame.key.get_pressed()  # Get the state of all keyboard keys

    if keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:  # Flap the bird
        bird_movey = -6

    WINDOW.blit(SKY, (0, 0))  # Draw the sky background

    pipe_x -= pipe_vel  # Move the pipe towards the bird

    # If the pipe reaches the left side of the screen, reset its position
    if pipe_x < -PIPE_WIDTH:
        pipe_x = WIDTH
        pipe_height = generate_pipe_height()  # Random height for the pipes
        pipe_y_bottom = pipe_height + pipe_gap  # Calculate the y position of the bottom pipe
        update_score()  # Update the score

    WINDOW.blit(PIPE_TOP, (pipe_x, pipe_height - PIPE_TOP.get_height()))  # Draw the top pipe
    WINDOW.blit(PIPE_BOTTOM, (pipe_x, pipe_y_bottom))  # Draw the bottom pipe

    ground.update()
    WINDOW.blit(ground.image, ground.rect)  # Draw the ground

    WINDOW.blit(BIRD, (bird_x, bird_y))  # Draw the bird at its updated position

    display_score()  # Display the score

    pygame.display.update()

    gravity()  # Apply gravity to the bird
    bird_y += bird_movey  # Update the bird's position with vertical movement

    # Ensure the bird stays within the screen bounds
    if bird_y < 0:  # Restrict going above y=0
        bird_y = 0
        bird_movey = 0
    elif bird_y > HEIGHT - BIRD_HEIGHT:  # Restrict going below y=height-BIRD_HEIGHT
        bird_y = HEIGHT - BIRD_HEIGHT
        bird_movey = 0

pygame.quit()