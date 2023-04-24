import pygame
import random
import time

class Level:
    def __init__(self, enemy_base_x, enemy_base_y, enemy_images, player_y, enemy_base_height):
        self.level = 1
        self.enemies = []
        self.player_y = player_y
        self.enemy_base_x = enemy_base_x
        self.enemy_base_y = enemy_base_y
        self.enemy_img = enemy_images
        self.enemy_base_height = enemy_base_height
        self.font = pygame.font.Font(None, 36)

    def draw_health_text(self, screen, x, y, health):
        health_text = self.font.render(f"{health}", True, (255, 255, 255))
        screen.blit(health_text, (x, y))

    def generate_enemies(self):
        num_enemies = 12 * (2 ** (self.level - 1))
        
        for i in range(num_enemies):
            enemy_type = 0
            
            if self.level >= 2 and i % 2 == 0:
                enemy_type = 1
                
            if self.level >= 4 and i % (self.level - 2) == 0:
                enemy_type = 2
                
            enemy = {
                "img": self.enemy_img[enemy_type],
                "x": self.enemy_base_x,
                "y": random.randint(self.enemy_base_y, self.enemy_base_y + self.enemy_base_height - self.enemy_img[enemy_type].get_height()),
                "speed": 1,
                "spawn_time": time.time() + random.uniform(1, 14),
                "health": 100 * (2 ** enemy_type)
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
                self.draw_health_text(screen, enemy["x"] - camera_x, enemy["y"] - 20, enemy["health"])

    def next_level(self):
        self.level += 1
        self.enemies.clear()
        self.generate_enemies()

    def draw_level_text(self, screen, x, y):
        level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        screen.blit(level_text, (x, y))

    def remove_enemies(self):
        self.enemies = [enemy for enemy in self.enemies if enemy["health"] > 0]
