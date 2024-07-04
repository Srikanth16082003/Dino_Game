import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game")

# Load Dino images
dino_img = pygame.image.load('dino.png')
dino_img = pygame.transform.scale(dino_img, (50, 50))
dino_rect = dino_img.get_rect()
dino_rect.y = GROUND_HEIGHT - dino_rect.height

# Load obstacle image
obstacle_img = pygame.image.load('obstacle.png')
obstacle_img = pygame.transform.scale(obstacle_img, (50, 50))

# Variables
dino_y = GROUND_HEIGHT - dino_rect.height
dino_vy = 0
gravity = 1
jump_strength = 15
is_jumping = False
score = 0
obstacles = []

# Function to draw the ground
def draw_ground():
    pygame.draw.line(screen, BLACK, (0, GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT), 2)

# Function to handle obstacle movement and generation
def handle_obstacles():
    global score

    # Generate new obstacle
    if random.randint(1, 100) <= 2:
        new_obstacle = obstacle_img.get_rect()
        new_obstacle.x = SCREEN_WIDTH
        new_obstacle.y = GROUND_HEIGHT - new_obstacle.height
        obstacles.append(new_obstacle)

    # Move obstacles and remove off-screen ones
    for obstacle in obstacles[:]:
        obstacle.x -= 10
        if obstacle.right < 0:
            obstacles.remove(obstacle)
            score += 1

# Function to handle collisions
def check_collisions():
    for obstacle in obstacles:
        if dino_rect.colliderect(obstacle):
            return True
    return False

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    draw_ground()
    handle_obstacles()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                dino_vy = -jump_strength
                is_jumping = True

    # Update Dino position
    dino_vy += gravity
    dino_y += dino_vy
    if dino_y >= GROUND_HEIGHT - dino_rect.height:
        dino_y = GROUND_HEIGHT - dino_rect.height
        dino_vy = 0
        is_jumping = False

    dino_rect.y = dino_y

    # Check for collisions
    if check_collisions():
        running = False

    # Draw Dino and obstacles
    screen.blit(dino_img, dino_rect)
    for obstacle in obstacles:
        screen.blit(obstacle_img, obstacle)

    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(50)

pygame.quit()
            