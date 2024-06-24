import pygame
from config import items_sprites


class Item:
    def __init__(self, name, icon_path, width=40, height=40):
        """Инициализирует предмет с заданным именем и иконкой."""
        self.name = name
        self.icon = pygame.image.load(icon_path).convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (width, height))


class Axe(Item):
    def __init__(self):
        """
        Инициализирует объект топора, унаследованный от класса Item.
        Загружает изображение иконки топора из файла.
        """
        super().__init__("Axe", f"{items_sprites}axe.png")


class Sword(Item):
    def __init__(self):
        """
        Инициализирует объект меча, унаследованный от класса Item.
        Загружает изображение иконки меча из файла.
        """
        super().__init__("Sword", f"../{items_sprites}sword.png")
