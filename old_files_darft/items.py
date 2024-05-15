import pygame
from old_files_darft.config import items_sprites


class Item:
    def __init__(self, name, icon_path, width=40, height=40):
        self.name = name
        self.icon = pygame.image.load(icon_path).convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (width, height))


class Axe(Item):
    def __init__(self):
        super().__init__("Axe", f"../{items_sprites}axe.png")


class Sword(Item):
    def __init__(self):
        super().__init__("Sword", f"../{items_sprites}sword.png")
