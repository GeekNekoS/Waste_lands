import pygame


class Inventory:
    def __init__(self, max_slots):
        self.max_slots = max_slots
        self.items = [None] * max_slots

    def __len__(self):
        return sum(1 for item in self.items if item is not None)

    def __getitem__(self, index):
        return self.items[index]

    def add_item(self, item):
        for i in range(self.max_slots):
            if not self.items[i]:
                self.items[i] = item
                return True
        return False


class InventorySlot:
    def __init__(self, rect):
        self.rect = rect

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)  # Отрисовка рамки слота


class InventoryPanel:
    def __init__(self, x, y, width, height, inventory):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inventory = inventory
        self.slot_width = 40  # Ширина слота
        self.slot_height = 40  # Высота слота
        self.slot_padding = 1  # Расстояние между слотами

    def draw(self, screen):
        # Отрисовка фона инвентаря
        panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (100, 100, 100), panel_rect)

        # Рассчитываем количество слотов по горизонтали и вертикали
        num_slots_horizontal = self.width // (self.slot_width + self.slot_padding)
        num_slots_vertical = self.height // (self.slot_height + self.slot_padding)

        # Рассчитываем ширину и высоту области, которая будет содержать все слоты
        total_width = num_slots_horizontal * self.slot_width + (num_slots_horizontal - 1) * self.slot_padding
        total_height = num_slots_vertical * self.slot_height + (num_slots_vertical - 1) * self.slot_padding

        # Рассчитываем координаты верхнего левого угла области слотов
        slots_x = self.x + (self.width - total_width) // 2
        slots_y = self.y + (self.height - total_height) // 2

        # Рисуем слоты
        for row in range(num_slots_vertical):
            for col in range(num_slots_horizontal):
                slot_x = slots_x + col * (self.slot_width + self.slot_padding)
                slot_y = slots_y + row * (self.slot_height + self.slot_padding)
                slot_rect = pygame.Rect(slot_x, slot_y, self.slot_width, self.slot_height)
                InventorySlot(slot_rect).draw(screen)  # Отрисовываем каждый слот
