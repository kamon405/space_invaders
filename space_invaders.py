import pygame
import random

# Initialize pygame
pygame.init()

# Set up display window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
bullet_img = pygame.image.load("bullet.png")

# Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5

    def draw(self):
        screen.blit(player_img, (self.x, self.y))

# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1

    def draw(self):
        screen.blit(enemy_img, (self.x, self.y))

# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10

    def draw(self):
        screen.blit(bullet_img, (self.x, self.y))

# Create enemies
def create_enemies(rows, cols, spacing):
    enemies = []
    for i in range(rows):
        for j in range(cols):
            x = j * (enemy_img.get_width() + spacing)
            y = i * (enemy_img.get_height() + spacing)
            enemy = Enemy(x, y)
            enemies.append(enemy)
    return enemies

# Check for bullet-enemy collisions
def check_collisions(bullets, enemies):
    score = 0
    for bullet in bullets:
        for enemy in enemies:
            if (bullet.x >= enemy.x and bullet.x <= enemy.x + enemy_img.get_width()) and (bullet.y >= enemy.y and bullet.y <= enemy.y + enemy_img.get_height()):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 100
                break
    return score

# Main game loop
player = Player(WIDTH // 2, HEIGHT - 100)
bullets = []
enemies = create_enemies(4, 10, 10)
score = 0
running = True
while running:
    screen.fill((0, 0, 0))

    # Handle user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.x + player_img.get_width() // 2 - bullet_img.get_width() // 2, player.y)
                bullets.append(bullet)

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player.speed
    if keys[pygame.K_RIGHT]:
        player.x += player.speed

    # Keep player within screen bounds
    if player.x <= 0:
        player.x = 0
    elif player.x >= WIDTH - player_img.get_width():
        player.x = WIDTH - player_img.get_width()

    # Update game objects
    # Move bullets
    for bullet in bullets:
        bullet.y -= bullet.speed
        if bullet.y < -bullet_img.get_height():
            bullets.remove(bullet)

    # Move enemies
    for enemy in enemies:
        enemy.x += enemy.speed
        if enemy.x <= 0 or enemy.x >= WIDTH - enemy_img.get_width():
            enemy.speed = -enemy.speed
            enemy.y += enemy_img.get_height()

    # Check collisions
    score += check_collisions(bullets, enemies)

    # Render game objects
    player.draw()
    for bullet in bullets:
        bullet.draw()
    for enemy in enemies:
        enemy.draw()

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.update()
    pygame.time.delay(10)

pygame.quit()
