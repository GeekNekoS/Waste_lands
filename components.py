import pygame


class Component:
    pass


class HitboxComponent(Component):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class PositionComponent(Component):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class VelocityComponent(Component):
    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy


class RenderComponent(Component):
    def __init__(self, image):
        self.image = image


class InventoryComponent(Component):
    def __init__(self, max_slots):
        self.inventory = []
        self.max_slots = max_slots

    def add_item(self, item):
        if len(self.inventory) < self.max_slots:
            self.inventory.append(item)
            return True
        return False
