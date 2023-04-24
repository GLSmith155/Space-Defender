import pygame

def resize_image(image, scale_factor):
    width, height = image.get_width() // scale_factor, image.get_height() // scale_factor
    return pygame.transform.scale(image, (width, height))

class Defense:
    def __init__(self, img_path, x, y, radius, damage, burst_damage, burst_rate, cost):
        self.image = img_path
        self.x = x
        self.y = y
        self.radius = radius
        self.damage = damage
        self.burst_damage = burst_damage
        self.burst_rate = burst_rate
        self.cost = cost
        self.time_since_last_burst = 0

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.x - camera_x, self.y - camera_y))
        surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255, 128), (self.radius, self.radius), self.radius, 2)
        screen.blit(surface, (self.x - self.radius + self.image.get_width() // 2 - camera_x, self.y - self.radius + self.image.get_height() // 2 - camera_y))

    def is_inside_radius(self, x, y):
        distance = ((self.x - x + self.image.get_width() // 2) ** 2 + (self.y - y + self.image.get_height() // 2) ** 2) ** 0.5
        return distance <= self.radius
