import pygame
import random
import os


class Component:
    pass


class InventoryComponent:
    def __init__(self, max_slots):
        self.max_slots = max_slots
        self.items = [None] * max_slots
        self.slot_width = 40
        self.slot_height = 40
        self.slot_padding = 2
        self.active_slot_index = None

    def draw_inventory(self, screen, width, height):
        # Определяем ширину и высоту панели инвентаря
        panel_width = self.max_slots * (self.slot_width + self.slot_padding) - self.slot_padding
        panel_height = self.slot_height + 2 * self.slot_padding

        # Рассчитываем координаты верхнего левого угла панели инвентаря
        panel_x = (width - panel_width) // 2
        panel_y = self.slot_padding

        # Отрисовка фона инвентаря
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, (100, 100, 100), panel_rect)

        # Рисуем слоты
        for i in range(self.max_slots):
            slot_x = panel_x + i * (self.slot_width + self.slot_padding) + self.slot_padding
            slot_y = panel_y + self.slot_padding
            slot_rect = pygame.Rect(slot_x, slot_y, self.slot_width, self.slot_height)
            if self.active_slot_index == i:
                pygame.draw.rect(screen, (255, 255, 255), slot_rect, 3)  # Отрисовываем активный слот
            else:
                pygame.draw.rect(screen, (255, 255, 255), slot_rect, 1)  # Отрисовываем обычный слот

            # Рисуем предметы в слотах инвентаря
            item = self.items[i]
            if item:
                screen.blit(item.icon, (slot_x, slot_y))

    def move_active_slot(self, direction):
        if self.active_slot_index is None:
            self.active_slot_index = 0
        else:
            self.active_slot_index += direction
            self.active_slot_index %= self.max_slots

    def update_inventory(self, new_inventory):
        # Обновляем инвентарь
        self.items = new_inventory

    def set_active_slot_index(self, index):
        # Устанавливаем индекс активной ячейки
        self.active_slot_index = index


class FootstepsComponent:
    def __init__(self):
        self.footstep_sounds = [
            pygame.mixer.Sound(os.path.join('sounds', 'footsteps', 'ground', f'step_{i}.wav'))
            for i in range(1, 13)
        ]
        self.current_sound = None
        self.volume = 0.5  # Начальная громкость звуков шагов

    def play_footstep(self, animation_component):
        current_frame_index = animation_component.current_frame
        if current_frame_index % 2 == 0:  # Проверяем, является ли текущий кадр четным
            if not pygame.mixer.get_busy():
                # Если ни один звук не проигрывается, выбираем новый звук и воспроизводим его
                self.current_sound = random.choice(self.footstep_sounds)
                self.current_sound.set_volume(self.volume)  # Устанавливаем громкость звука
                self.current_sound.play()


class SoundComponent(Component):
    def __init__(self, sound_file):
        self.sound = pygame.mixer.Sound(sound_file)

    def play(self):
        self.sound.play()


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


class AnimationComponent(Component):
    def __init__(self, frames, frame_rate):
        self.frames = frames
        self.frame_rate = frame_rate
        self.current_frame = 0
        self.time_since_last_frame = 0

    def update(self, dt):
        self.time_since_last_frame += dt
        if self.time_since_last_frame >= self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.time_since_last_frame = 0

    def get_current_frame(self):
        return self.frames[self.current_frame]
