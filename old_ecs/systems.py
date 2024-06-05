import pygame
from old_ecs.components import (
    PositionComponent,
    VelocityComponent,
    RenderComponent,
    InventoryComponent,
    MenuComponent
)


class System:
    def update(self, entities, *args, **kwargs):
        raise NotImplementedError


class MenuSystem:
    def __init__(self):
        pass

    def update(self, entities, events):
        for entity in entities:
            menu_component = entity.get_component(MenuComponent)
            if menu_component:
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            menu_component.selected_option -= 1
                        elif event.key == pygame.K_DOWN:
                            menu_component.selected_option += 1


class MovementSystem(System):
    def update(self, entities):
        for entity in entities:
            pos = entity.get_component(PositionComponent)
            vel = entity.get_component(VelocityComponent)
            if pos and vel:
                pos.x += vel.vx
                pos.y += vel.vy

    def handle_menu_controls(self, entities, key_pressed):
        for entity in entities:
            menu_component = entity.get_component(MenuComponent)
            if menu_component:
                if key_pressed[pygame.K_UP]:
                    menu_component.move_selection(-1)
                elif key_pressed[pygame.K_DOWN]:
                    menu_component.move_selection(1)


class RenderSystem(System):
    def __init__(self):
        pass

    def update(self, entities, screen):
        for entity in entities:
            pos = entity.get_component(PositionComponent)
            render = entity.get_component(RenderComponent)
            if pos and render and isinstance(render.image, pygame.surface.Surface):
                screen.blit(render.image, (pos.x, pos.y))

    def render_menu(self, screen, menu_entities, menu_visible):
        if menu_visible:
            for entity in menu_entities:
                menu_component = entity.get_component(MenuComponent)
                if menu_component:
                    position_component = entity.get_component(PositionComponent)
                    if position_component:
                        menu_font = pygame.font.Font(None, 36)
                        menu_width = 0
                        menu_height = len(menu_component.items) * 50
                        for item in menu_component.items:
                            menu_text = menu_font.render(item, True, (255, 255, 255))
                            text_width, _ = menu_text.get_size()
                            menu_width = max(menu_width, text_width)
                        x = (screen.get_width() - menu_width) // 2
                        y = (screen.get_height() - menu_height) // 2
                        for i, item in enumerate(menu_component.items):
                            menu_text = menu_font.render(item, True, (255, 255, 255))
                            screen.blit(menu_text, (x, y + i * 50))

    def draw_menu(self, screen, menu_component):
        font = pygame.font.Font(None, 36)
        menu_position = menu_component.position

        for index, option in enumerate(menu_component.options):
            text_surface = font.render(option, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.center = (menu_position[0], menu_position[1] + index * 40)
            screen.blit(text_surface, text_rect)

            if index == menu_component.selected_option:
                pygame.draw.rect(screen, (255, 0, 0), text_rect, 2)


class CollisionSystem(System):
    def __init__(self, quadtree):
        self.quadtree = quadtree

    def update(self, entities):
        for entity in entities:
            pos = entity.get_component(PositionComponent)
            # Implement collision detection logic here


class InventorySystem:
    def __init__(self):
        pass

    def update(self, entities, screen):
        for entity in entities:
            inventory_component = entity.get_component(InventoryComponent)
            position_component = entity.get_component(PositionComponent)
            if inventory_component and position_component:
                inventory_component.draw_inventory(screen, position_component.x, position_component.y)
