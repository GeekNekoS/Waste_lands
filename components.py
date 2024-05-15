import pygame
import random
import os


class Component:
    pass


class FootstepsComponent:
    def __init__(self):
        self.footstep_sounds = [
            pygame.mixer.Sound(os.path.join('sounds', 'footsteps', 'ground', f'step_{i}.wav'))
            for i in range(1, 13)
        ]
        self.current_sound = None
        self.volume = 0.15  # Начальная громкость звуков шагов

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


class InventoryComponent(Component):
    def __init__(self, max_slots):
        self.inventory = []
        self.max_slots = max_slots

    def add_item(self, item):
        if len(self.inventory) < self.max_slots:
            self.inventory.append(item)
            return True
        return False
