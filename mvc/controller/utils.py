import pygame
import random
from settings import WIDTH, HEIGHT
import math


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def draw_debug_line(screen, player_rect, item_rect, camera_x, camera_y):
    # Рассчитываем координаты центров прямоугольников с учетом смещения камеры
    player_center = (player_rect.centerx - camera_x, player_rect.centery - camera_y)
    item_center = (item_rect.centerx - camera_x, item_rect.centery - camera_y)

    # Рисуем линию от игрока до предмета
    pygame.draw.line(screen, (255, 0, 0), player_center, item_center, 1)


def draw_debug_line_to_tree(screen, player_rect, trees, camera_x, camera_y):
    # Получаем центр хитбокса игрока с учетом смещения камеры
    player_center = (player_rect.centerx - camera_x, player_rect.centery - camera_y)
    closest_tree = None
    min_distance = float('inf')

    # Находим ближайшее дерево
    for image_rect, hitbox_rect in trees:
        tree_center = (hitbox_rect.centerx - camera_x, hitbox_rect.centery - camera_y)
        distance = ((player_center[0] - tree_center[0]) ** 2 + (player_center[1] - tree_center[1]) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest_tree = tree_center

    # Если ближайшее дерево найдено, рисуем линию от игрока до него
    if closest_tree:
        pygame.draw.line(screen, (0, 255, 0), player_center, closest_tree, 1)
        # print(f"Drawing line to tree at {closest_tree}")
    else:
        print("No tree found!")


# Линия до всех деревьев на карте
# def draw_debug_line_to_tree(screen, player_rect, trees, camera_x, camera_y):
#     # Получаем центр хитбокса игрока с учетом смещения камеры
#     player_center = (player_rect.centerx - camera_x, player_rect.centery - camera_y)
#
#     # Рисуем линию от игрока до каждого дерева
#     for image_rect, hitbox_rect in trees:
#         tree_center = (hitbox_rect.centerx - camera_x, hitbox_rect.centery - camera_y)
#         pygame.draw.line(screen, (0, 255, 0), player_center, tree_center, 1)


def detect_item_pickup(player_rect, item_rect):
    # Проверяем, пересекается ли игрок с предметом
    if player_rect.colliderect(item_rect):
        return True
    return False


def play_background_music():
    pygame.mixer.init()
    pygame.mixer.music.load('sounds/dark-background-sounds.mp3')
    pygame.mixer.music.play(-1)
