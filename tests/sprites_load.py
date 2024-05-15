import pygame


# Проверка загрузки изображений
print("Проверка загрузки изображений...")
try:
    pygame.image.load('../sprites/player/down_1.png')
    pygame.image.load('../sprites/tree.png')
    print("Изображения успешно загружены.")
except pygame.error as e:
    print("Ошибка загрузки изображений:", e)
