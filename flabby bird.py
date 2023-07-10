import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 609, 663
BIRD_HEIGHT = 110
BIRD_WIDTH = 110
VEL = 5
PIPE_WIDTH = 100
pipe_vel = 6
SCORE = 0

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

SKY = pygame.image.load(os.path.join('flappy bird', 'imgs', 'skyd.png'))
ground_image = pygame.image.load(os.path.join('flappy bird', 'imgs', 'sky_bottom.png'))
restart = pygame.image.load(os.path.join('flappy bird', 'imgs', 'restart.png'))
BG = pygame.image.load(os.path.join('flappy bird', 'imgs', 'BG.png'))
SOUND = pygame.mixer.Sound(os.path.join('flappy bird', 'imgs', 'coin.wav'))
MS = pygame.image.load(os.path.join('flappy bird', 'imgs', 'message.png'))

ground_width = ground_image.get_width()

def main_menu():
    while True:
        WINDOW.blit(BG, (0, 0))
        WINDOW.blit(MS, (207, 170))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                    return

        pygame.display.update()

def display_score():
    font = pygame.font.Font(os.path.join('flappy bird', 'imgs', 'font.otf'), 55)
    text = font.render(str(SCORE), True, (0, 0, 0))
    WINDOW.blit(text, (295, 90))

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

PIPE_TOP = pygame.image.load(os.path.join('flappy bird', 'imgs', 'pipe_top.png'))
PIPE_BOTTOM = pygame.image.load(os.path.join('flappy bird', 'imgs', 'pipe_bottom.png'))

BIRD = pygame.image.load(os.path.join('flappy bird', 'imgs', 'bird.png'))
BIRD = pygame.transform.scale(BIRD, (BIRD_WIDTH, BIRD_HEIGHT))

bird_x = WIDTH // 2 - BIRD_WIDTH // 2
bird_y = HEIGHT // 2 - BIRD_HEIGHT // 2

bird_movey = 0
bird_gravity = 0.4
collision_gravity = 4
jump_velocity = -7

pipe_x = WIDTH + PIPE_WIDTH
pipe_gap = 200

def generate_pipe_height():
    min_height = 100
    max_height = HEIGHT - pipe_gap - min_height - BIRD_HEIGHT
    return random.randint(min_height, max_height)

pipe_height = generate_pipe_height()
pipe_y_bottom = pipe_height + pipe_gap

def gravity():
    global bird_movey
    bird_movey += bird_gravity

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

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] == 1 and self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))


button = Button(WIDTH // 2 - 65, HEIGHT // 2 - 15, restart)

running = True
clock = pygame.time.Clock()
game_over = False
falling = True
bird_gravity = 0.4
collision_gravity = 8
jump_velocity = -7
game_started = False

def restart_game():
    global bird_y, bird_movey, pipe_x, pipe_height, pipe_y_bottom, SCORE, game_over, falling, pipe_vel, game_started
    bird_y = HEIGHT // 2 - BIRD_HEIGHT // 2
    bird_movey = 0
    pipe_x = WIDTH + PIPE_WIDTH
    pipe_height = generate_pipe_height()
    pipe_y_bottom = pipe_height + pipe_gap
    SCORE = 0
    game_over = False
    falling = True
    pipe_vel = 5
    game_started = False

main_menu()  # Show the main menu screen initially

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys_pressed = pygame.key.get_pressed()

    if not game_started:
        if keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP] or pygame.mouse.get_pressed()[0] == 1:
            game_started = True
            continue

    if game_started and not game_over:
        if keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            bird_movey = jump_velocity

    if game_started and not game_over:
        if check_collision():
            falling = True
            bird_movey = collision_gravity
            pipe_vel = 0

        if falling:
            bird_movey += bird_gravity

        pipe_x -= pipe_vel

        if pipe_x < -PIPE_WIDTH:
            pipe_x = WIDTH
            pipe_height = generate_pipe_height()
            pipe_y_bottom = pipe_height + pipe_gap
            pygame.mixer.Sound.play(SOUND)
            pygame.mixer.music.stop()
            update_score()

        WINDOW.blit(SKY, (0, 0))
        WINDOW.blit(PIPE_TOP, (pipe_x, pipe_height - PIPE_TOP.get_height()))
        WINDOW.blit(PIPE_BOTTOM, (pipe_x, pipe_y_bottom))
        ground.update()
        WINDOW.blit(ground.image, ground.rect)
        WINDOW.blit(BIRD, (bird_x, bird_y))
        display_score()
        pygame.display.update()
        bird_y += bird_movey

        if bird_y >= 487.21:
            game_over = True

        if bird_y < 0:
            bird_y = 0
            bird_movey = 0
        elif bird_y > HEIGHT - BIRD_HEIGHT:
            bird_y = HEIGHT - BIRD_HEIGHT
            bird_movey = 0
            if not game_over:
                game_over = True

    if game_over:
        bird_movey = collision_gravity
        pipe_vel = 0

        if button.draw(WINDOW):
            restart_game()

        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(mouse_pos):
            restart_game()

        bird_y += bird_movey

        if bird_y >= HEIGHT - BIRD_HEIGHT:
            game_over_text = pygame.image.load(os.path.join('flappy bird', 'imgs', 'gameover.png'))
            WINDOW.blit(game_over_text, (200, 255))

    pygame.display.update()

pygame.quit()

