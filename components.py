import pygame


class Component:
    pass


class HitboxComponent:
    def __init__(self, x_offset, y_offset, width, height):
        self.x_offset = x_offset  # Смещение по оси X относительно позиции сущности
        self.y_offset = y_offset  # Смещение по оси Y относительно позиции сущности
        self.width = width  # Ширина хитбокса
        self.height = height  # Высота хитбокса

    def get_rect(self, position):
        # Создаем прямоугольник хитбокса с учетом смещения и позиции сущности
        return pygame.Rect(position.x + self.x_offset, position.y + self.y_offset, self.width, self.height)

    def set_offset(self, x_offset, y_offset):
        self.x_offset = x_offset
        self.y_offset = y_offset


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
