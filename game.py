import pygame
import sys
import random
import time
from levels import Level
from defenses import Defense

def resize_image(image, scale_factor):
    width, height = image.get_width() // scale_factor, image.get_height() // scale_factor
    return pygame.transform.scale(image, (width, height))

pygame.init()

WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Defense")

player_img = resize_image(pygame.image.load("player_image.png"), 3)
enemy_base_img = pygame.image.load("enemy_base.png")
enemy_img1 = resize_image(pygame.image.load("enemy1.png"), 13)
enemy_img2 = resize_image(pygame.image.load("enemy2.png"), 13)
enemy_img3 = resize_image(pygame.image.load("enemy3.png"), 10)
enemy_images = [enemy_img1, enemy_img2, enemy_img3]  
background_img = pygame.image.load("background_image.jpg")
game_over_img = resize_image(pygame.image.load("game_over_image.png"), 5)
defense1 = resize_image(pygame.image.load("defense1.png"), 10)
defense2 = resize_image(pygame.image.load("defense2.png"), 28)
defense3 = resize_image(pygame.image.load("defense3.png"), 12)

player_x, player_y = 0, HEIGHT // 2 - player_img.get_height() // 2
map_width = max(WIDTH * 2, enemy_base_img.get_width())
enemy_base_x, enemy_base_y = map_width - enemy_base_img.get_width() - 100, HEIGHT // 2 - enemy_base_img.get_height() // 2

camera = pygame.Rect(0, 0, WIDTH, HEIGHT)
camera.centerx = enemy_base_x - WIDTH // 2

level_manager = Level(enemy_base_x, enemy_base_y, enemy_images, player_y/2, enemy_base_img.get_height())
level_manager.generate_enemies()

player_health = 100
resources = 200
tower_costs = [25, 100, 300]
font = pygame.font.Font(None, 36)

running = True
game_over = False
placing_defense = False
selected_defense = None
defenses = []
waiting_for_next_level = False
tower_info_text = font.render("Press 1, 2, or 3 to place towers (50, 200, or 500 resources).", True, (255, 255, 255))
press_enter_text = font.render("Press ENTER to proceed to the next level.", True, (255, 255, 255))

while running:
    elapsed_time = pygame.time.Clock().tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not placing_defense:
                if event.key == pygame.K_1 and resources >= 50:
                    placing_defense = True
                    selected_defense = Defense(defense1, 0, 0, 150, 0, 6, .1, 50)
                elif event.key == pygame.K_2 and resources >= 200:
                    placing_defense = True
                    selected_defense = Defense(defense2, 0, 0, 100, 0, 40, .3, 200)
                elif event.key == pygame.K_3 and resources >= 500:
                    placing_defense = True
                    selected_defense = Defense(defense3, 0, 0, 50, 0, 200, 0.2, 500)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if placing_defense and selected_defense is not None:
                defenses.append(Defense(selected_defense.image, selected_defense.x, selected_defense.y, selected_defense.radius, selected_defense.damage, selected_defense.burst_damage, selected_defense.burst_rate, selected_defense.cost))
                resources -= selected_defense.cost
                placing_defense = False
                selected_defense = None

    mouse_x, mouse_y = pygame.mouse.get_pos()
    camera.centerx = max(min(mouse_x, map_width - WIDTH // 2), WIDTH // 2)

    screen.blit(background_img, (0, 0), camera)

    # I removed the enemy base image, but will leave this here in case I decide to re-add.
    #screen.blit(enemy_base_img, (enemy_base_x - camera.x, enemy_base_y))

    level_manager.move_enemies()
    level_manager.draw_enemies(screen, camera.x)

    for enemy in list(level_manager.enemies):
        enemy_destroyed_by_tower = False
        for defense in defenses:
            if defense.is_inside_radius(enemy["x"], enemy["y"]):
                if defense.burst_damage == 0:
                    enemy["health"] -= defense.damage * elapsed_time
                else:
                    defense.time_since_last_burst += elapsed_time
                    if defense.time_since_last_burst >= defense.burst_rate:
                        enemy["health"] -= defense.burst_damage
                        defense.time_since_last_burst = 0

                if enemy["health"] <= 0:
                    enemy_destroyed_by_tower = True
                    level_manager.enemies.remove(enemy)
                    break
        if enemy_destroyed_by_tower:
            resources += 23

    if not level_manager.enemies and not waiting_for_next_level:
        pygame.display.update()
        waiting_for_next_level = True
        screen.blit(press_enter_text, (WIDTH // 2 - press_enter_text.get_width() // 2, HEIGHT - 40))
        pygame.display.update()

        enter_pressed = False
        while not enter_pressed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    enter_pressed = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        level_manager.next_level()
                        waiting_for_next_level = False
                        enter_pressed = True


    for defense in defenses:
        defense.draw(screen, camera.x, camera.y)

    if placing_defense and selected_defense is not None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        selected_defense.x = mouse_x - selected_defense.image.get_width() // 2
        selected_defense.y = mouse_y - selected_defense.image.get_height() // 2
        selected_defense.draw(screen, camera.x, camera.y)

    for enemy in level_manager.enemies:
        if enemy["x"] <= player_x + player_img.get_width() and not game_over:
            player_health -= 10
            level_manager.enemies.remove(enemy)

            if player_health <= 0:
                game_over = True

    screen.blit(player_img, (player_x - camera.x, player_y))

    health_text = font.render(f"Health: {player_health}", True, (2, 239, 106))
    screen.blit(health_text, (WIDTH - 150, 10))

    resources_text = font.render(f"Resources: {resources}", True, (255, 255, 255))
    screen.blit(resources_text, (WIDTH // 2 - resources_text.get_width() // 2, 10))

    level_manager.draw_level_text(screen, 10, 10)

    if game_over:
        screen.blit(game_over_img, (WIDTH // 2 - game_over_img.get_width() // 2, HEIGHT // 2 - game_over_img.get_height() // 2))
        pygame.display.update()
        time.sleep(4)
        pygame.quit()

    screen.blit(tower_info_text, (10, HEIGHT - 40))

    pygame.display.update()

pygame.quit()

