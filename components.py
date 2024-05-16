import pygame
import random
import os
import sys


class Component:
    pass


class TreeComponent(Component):
    pass


class IconComponent(Component):
    def __init__(self, icon):
        self.icon = icon


class AxeComponent(Component):
    def __init__(self):
        self.name = "Axe"
        original_image = pygame.image.load('sprites/items/axe.png')
        scaled_image = pygame.transform.scale(original_image, (int(original_image.get_width() * 0.5), int(original_image.get_height() * 0.5)))
        self.icon = scaled_image


class MenuComponent(Component):
    def __init__(self, items, options, position):
        self.items = items
        self.options = options
        self.position = position
        self.selected_option = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                selected_item = self.options[self.selected_option]
                if selected_item == "Start":
                    return "game"
                elif selected_item == "Options":
                    # Логика для перехода к экрану опций
                    pass
                elif selected_item == "Quit":
                    pygame.quit()
                    sys.exit()
        return None

    def draw(self, screen):
        menu_font = pygame.font.Font(None, 36)
        for i, item in enumerate(self.items):
            color = (255, 255, 255)
            if i == self.selected_option:
                color = (255, 0, 0)  # Цвет выделенного пункта меню
            menu_text = menu_font.render(item, True, color)
            x = self.position[0]
            y = self.position[1] + i * 50
            screen.blit(menu_text, (x, y))

    def move_selection(self, direction):
        self.selected_option = (self.selected_option + direction) % len(self.options)


class InventoryComponent(Component):
    def __init__(self, max_slots):
        self.max_slots = max_slots
        self.items = [None] * max_slots
        self.slot_width = 40
        self.slot_height = 40
        self.slot_padding = 2
        self.active_slot_index = None

    def add_item(self, item):
        item_component = item.get_component(RenderComponent)  # Получаем компонент RenderComponent из предмета
        if item_component:
            # Проверяем, есть ли пустые слоты в инвентаре
            for i in range(self.max_slots):
                if self.items[i] is None:
                    self.items[i] = item_component
                    print(f"Item added to slot {i}")
                    return True
        return False

    def draw_inventory(self, screen, width, height):
        panel_width = self.max_slots * (self.slot_width + self.slot_padding) - self.slot_padding
        panel_height = self.slot_height + 2 * self.slot_padding

        panel_x = (width - panel_width) // 2
        panel_y = self.slot_padding

        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, (100, 100, 100), panel_rect)

        for i in range(self.max_slots):
            slot_x = panel_x + i * (self.slot_width + self.slot_padding)
            slot_y = panel_y + self.slot_padding
            slot_rect = pygame.Rect(slot_x, slot_y, self.slot_width, self.slot_height)
            if self.active_slot_index == i:
                pygame.draw.rect(screen, (255, 255, 255), slot_rect, 3)
            else:
                pygame.draw.rect(screen, (255, 255, 255), slot_rect, 1)

            item = self.items[i]
            if item:
                if hasattr(item, 'get_component'):  # Проверяем, что item имеет метод get_component
                    axe_component = item.get_component(AxeComponent)
                    if axe_component and axe_component.icon:
                        screen.blit(axe_component.icon, (slot_x, slot_y))
                    print(f"Slot {i} contains item: {axe_component}")
                else:
                    print(f"Slot {i} contains item: {item}")  # Выводим информацию о RenderComponent
            else:
                print(f"Slot {i} is empty")

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


class FootstepsComponent(Component):
    def __init__(self):
        self.footstep_sounds = [
            pygame.mixer.Sound(os.path.join('sounds', 'footsteps', 'ground', f'step_{i}.wav'))
            for i in range(1, 9)
        ]
        self.current_sound = None
        self.volume = 0.25  # Начальная громкость звуков шагов

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


class HitboxComponent(Component):
    def __init__(self, width, height, offset_x=0, offset_y=0):
        super().__init__()
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y

    def get_rect(self, position):
        # Создаем прямоугольник хитбокса с учетом смещения и позиции сущности
        return pygame.Rect(position.x + self.offset_x, position.y + self.offset_y, self.width, self.height)

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
