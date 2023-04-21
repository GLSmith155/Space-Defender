import pygame
import sys
import random
from levels import Level

def resize_image(image, scale_factor):
    width, height = image.get_width() // scale_factor, image.get_height() // scale_factor
    return pygame.transform.scale(image, (width, height))

# Initialize Pygame
pygame.init()

# Define the game window dimensions and create the window
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Defense")

# Load the images for the player, enemy base, background, and game over
player_img = resize_image(pygame.image.load("player_image.png"), 5)
enemy_base_img = pygame.image.load("enemy_base.png")
enemy_img_path = "enemy_base.png"
enemy_img = pygame.image.load("enemy_base.png")
background_img = pygame.image.load("background_image.jpg")
game_over_img = resize_image(pygame.image.load("game_over_image.png"), 5)

# Set the player's position to the far left center of the screen
player_x, player_y = 0, HEIGHT // 2 - player_img.get_height() // 2

# Set the enemy base position to the far right center of the screen
map_width = max(WIDTH * 2, enemy_base_img.get_width())
enemy_base_x, enemy_base_y = map_width - enemy_base_img.get_width() - 100, HEIGHT // 2 - enemy_base_img.get_height() // 2

# Create a camera
camera = pygame.Rect(0, 0, WIDTH, HEIGHT)
camera.centerx = enemy_base_x - WIDTH // 2

# Create a level manager
level_manager = Level(enemy_base_x, enemy_base_y, enemy_img_path, player_y)
level_manager.generate_enemies()

# Initialize the player health
player_health = 100

# Set the font for displaying health
font = pygame.font.Font(None, 36)

# Define the game loop
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Update the camera position based on the mouse position
    camera.centerx = max(min(mouse_x, map_width - WIDTH // 2), WIDTH // 2)

    # Draw the background
    screen.blit(background_img, (0, 0), camera)

    # Draw the enemy base
    screen.blit(enemy_base_img, (enemy_base_x - camera.x, enemy_base_y))

    # Update and draw enemies
    level_manager.move_enemies()
    level_manager.draw_enemies(screen, camera.x)

    # Check if enemies have reached the player
    for enemy in level_manager.enemies:
        if enemy["x"] <= player_x + player_img.get_width() and not game_over:
            player_health -= 10
            level_manager.enemies.remove(enemy)

            if player_health <= 0:
                game_over = True

    # Draw the player
    screen.blit(player_img, (player_x - camera.x, player_y))

    # Draw the health text
    health_text = font.render(f"Health: {player_health}", True, (2, 239, 106))
    screen.blit(health_text, (WIDTH - 150, 10))

    # Draw the level text
    level_manager.draw_level_text(screen, 10, 10)

    if game_over:
        screen.blit(game_over_img, (WIDTH // 2 - game_over_img.get_width() // 2, HEIGHT // 2 - game_over_img.get_height() // 2))

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()