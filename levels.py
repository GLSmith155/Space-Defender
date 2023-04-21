import pygame
import random
import time

class Level:
    def __init__(self, enemy_base_x, enemy_base_y, enemy_img_path, player_y):
        self.level = 1
        self.enemies = []
        self.player_y = player_y
        self.enemy_base_x = enemy_base_x
        self.enemy_base_y = enemy_base_y
        self.enemy_img = pygame.image.load(enemy_img_path)
        self.font = pygame.font.Font(None, 36)

    def generate_enemies(self):
        num_enemies = 12 * (2 ** (self.level - 1))
        for _ in range(num_enemies):
            enemy = {
                "img": self.enemy_img,
                "x": self.enemy_base_x,
                "y": self.player_y,
                "speed": 15,
                "spawn_time": time.time() + random.uniform(2, 6)
            }
            self.enemies.append(enemy)

    def move_enemies(self):
        for enemy in self.enemies:
            if time.time() >= enemy["spawn_time"]:
                enemy["x"] -= enemy["speed"]

    def draw_enemies(self, screen, camera_x):
        for enemy in self.enemies:
            if time.time() >= enemy["spawn_time"]:
                screen.blit(enemy["img"], (enemy["x"] - camera_x, enemy["y"]))


    def next_level(self):
        self.level += 1
        self.enemies.clear()
        self.generate_enemies()

    def draw_level_text(self, screen, x, y):
        level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        screen.blit(level_text, (x, y))