import pygame
import random
from settings import WIDTH, HEIGHT


def draw_debug_line(screen, player_rect, item_rect, camera_x, camera_y):
    # Рассчитываем координаты центров прямоугольников с учетом смещения камеры
    player_center = (player_rect.centerx - camera_x, player_rect.centery - camera_y)
    item_center = (item_rect.centerx - camera_x, item_rect.centery - camera_y)

    # Рисуем линию от игрока до предмета
    pygame.draw.line(screen, (255, 0, 0), player_center, item_center, 1)


def detect_item_pickup(player_rect, axe_rect, player_inventory, axe):
    if axe_rect.colliderect(player_rect):
        player_inventory.add_item(axe)
        axe_rect.x = random.randint(0, WIDTH - axe.icon.get_width())
        axe_rect.y = random.randint(0, HEIGHT - axe.icon.get_height())


def play_background_music():
    pygame.mixer.init()
    pygame.mixer.music.load('../sounds/dark-background-sounds.mp3')
    pygame.mixer.music.play(-1)
