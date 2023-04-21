import pygame


class Enemy:
    def __init__(self, x, y, image, speed):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.speed = speed
        self.health = 100

    def move(self):
        self.x -= self.speed

    def draw(self, screen, camera_x):
        # Set the font for displaying health
        font = pygame.font.Font(None, 36)
        # Draw the health bar and text
        bar_length = 40
        bar_height = 5
        bar_x = self.x - camera_x + self.image.get_width() / 2 - bar_length / 2
        bar_y = self.y - 10
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_length, bar_height))
        health_text = font.render(f"Health: {self.health}", True, (255, 255, 255))
        screen.blit(health_text, (bar_x, bar_y - 20))

        # Draw the enemy image
        screen.blit(self.image, (self.x - camera_x, self.y))

    def has_reached_player(self, player_x):
        return self.x <= player_x
