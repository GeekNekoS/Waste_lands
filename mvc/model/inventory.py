import pygame


class Inventory:
    def __init__(self, max_slots):
        """Инициализирует инвентарь с заданным количеством слотов."""
        self.max_slots = max_slots
        self.items = [None] * max_slots

    def __len__(self):
        """Возвращает текущее количество предметов в инвентаре."""
        return sum(1 for item in self.items if item is not None)

    def __getitem__(self, index):
        """Возвращает предмет из указанного слота инвентаря."""
        return self.items[index]

    def add_item(self, item):
        """Добавляет предмет в первый доступный слот инвентаря."""
        for i in range(self.max_slots):
            if not self.items[i]:
                self.items[i] = item
                return True
        return False


class InventorySlot:
    def __init__(self, rect):
        """Инициализирует слот инвентаря с заданным прямоугольником для отрисовки."""
        self.rect = rect

    def draw(self, screen):
        """Отрисовывает рамку слота инвентаря на экране."""
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)  # Отрисовка рамки слота


class InventoryPanel:
    def __init__(self, x, y, width, height, inventory):
        """Инициализирует панель инвентаря с заданными параметрами."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inventory = inventory
        self.slot_width = 40  # Ширина слота
        self.slot_height = 40  # Высота слота
        self.slot_padding = 1  # Расстояние между слотами
        self.active_slot_index = None  # Индекс активной ячейки

    def draw(self, screen):
        """Отрисовывает панель инвентаря на экране."""
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
                if self.active_slot_index is not None and self.active_slot_index == row * num_slots_horizontal + col:
                    pygame.draw.rect(screen, (255, 255, 255), slot_rect, 3)  # Отрисовываем активную ячейку
                else:
                    pygame.draw.rect(screen, (255, 255, 255), slot_rect, 1)  # Отрисовываем обычную ячейку

                # Рисуем предметы в слотах инвентаря
                for i, item in enumerate(self.inventory):
                    slot_x = slots_x + (i % num_slots_horizontal) * (self.slot_width + self.slot_padding)
                    slot_y = slots_y + (i // num_slots_horizontal) * (self.slot_height + self.slot_padding)
                    item_rect = pygame.Rect(slot_x, slot_y, self.slot_width, self.slot_height)

                    # Определяем, является ли текущий слот активным
                    is_active_slot = (self.active_slot_index is not None) and (self.active_slot_index == i)

                    # Рисуем рамку вокруг активного слота
                    if is_active_slot:
                        pygame.draw.rect(screen, (255, 0, 0), item_rect, 3)
                    else:
                        pygame.draw.rect(screen, (255, 255, 255), item_rect, 1)

                    # Рисуем предмет в слоте
                    if item:
                        screen.blit(item.icon, item_rect)

    def update_inventory(self, new_inventory):
        """Обновляет инвентарь новым списком предметов."""
        self.inventory = new_inventory

    def set_active_slot_index(self, index):
        """Устанавливает индекс активной ячейки в инвентаре."""
        self.active_slot_index = index
