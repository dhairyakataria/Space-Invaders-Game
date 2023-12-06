import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SPEED = 6
ENEMY_COUNT = 4

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)

# Load images
background = pygame.image.load("background.png")
player_img = pygame.image.load('player.png')
enemy_img = [pygame.image.load('enemy.png') for _ in range(ENEMY_COUNT)]
bullet_img = pygame.image.load('bullet.png')

# Player
player_x = 378
player_y = 500
player_x_change = 0

# Enemies
enemy_x = [random.randint(0, 736) for _ in range(ENEMY_COUNT)]
enemy_y = [random.randint(50, 150) for _ in range(ENEMY_COUNT)]
enemy_x_change = [5 for _ in range(ENEMY_COUNT)]
enemy_y_change = [40 for _ in range(ENEMY_COUNT)]

# Bullet
bullet_x = 0
bullet_y = 500
bullet_y_change = -10
bullet_state = 0

# Score
font = pygame.font.Font('freesansbold.ttf', 32)
score_val = 0

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Function to handle player movement
def handle_player_movement():
    global player_x, player_x_change
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x_change = -PLAYER_SPEED
    elif keys[pygame.K_RIGHT]:
        player_x_change = PLAYER_SPEED
    else:
        player_x_change = 0
    player_x += player_x_change
    if player_x < 0:
        player_x = 0
    elif player_x > 736:
        player_x = 736

# Function to handle enemy movement
def handle_enemy_movement():
    global score_val
    global bullet_y
    for i in range(ENEMY_COUNT):
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] < 0:
            enemy_x[i] = 0
            enemy_y[i] += enemy_y_change[i]
            enemy_x_change[i] = -enemy_x_change[i]
        elif enemy_x[i] > 736:
            enemy_x[i] = 736
            enemy_y[i] += enemy_y_change[i]
            enemy_x_change[i] = -enemy_x_change[i]
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 500
            bullet_state = 0
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(25, 150)
            score_val += 1

# Function to handle bullet movement and collisions
def handle_bullet():
    global bullet_y, bullet_state
    if bullet_y <= 0:
        bullet_y = 500
        bullet_state = 0
    if bullet_state == 1:
        bullet(bullet_x, bullet_y)
        bullet_y += bullet_y_change

# Function to display score
def display_score():
    score = font.render("Score : " + str(score_val), True, (220, 220, 220))
    screen.blit(score, (10, 10))

# Function to display game over text
def display_game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Function to display player
def player(x, y):
    screen.blit(player_img, (x, y))

# Function to display enemy
def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

# Function to display bullet
def bullet(x, y):
    global bullet_state
    bullet_state = 1
    screen.blit(bullet_img, (x + 16, y + 10))

# Function to check collision
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == 0:
                    bullet_x = player_x
                    bullet(bullet_x, bullet_y)
    
    handle_player_movement()
    handle_bullet()
    handle_enemy_movement()
    display_score()
    player(player_x, player_y)
    for i in range(ENEMY_COUNT):
        enemy(enemy_x[i], enemy_y[i], i)
        if enemy_y[i] > 460:
            display_game_over_text()
            running = False  # Stop the game loop when an enemy reaches a certain position
            break  # Break the loop after displaying the game over text


    pygame.display.update()
