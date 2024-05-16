import pygame
from components import (
    PositionComponent,
    VelocityComponent,
    RenderComponent,
    InventoryComponent
)


class System:
    def update(self, entities, *args, **kwargs):
        raise NotImplementedError


class MovementSystem(System):
    def update(self, entities):
        for entity in entities:
            pos = entity.get_component(PositionComponent)
            vel = entity.get_component(VelocityComponent)
            if pos and vel:
                pos.x += vel.vx
                pos.y += vel.vy


class RenderSystem(System):
    def update(self, entities, screen):
        for entity in entities:
            pos = entity.get_component(PositionComponent)
            render = entity.get_component(RenderComponent)
            if pos and render and isinstance(render.image, pygame.surface.Surface):
                screen.blit(render.image, (pos.x, pos.y))


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
            position_component = entity.get_component(PositionComponent)  # Предположим, что у инвентаря есть позиция
            if inventory_component and position_component:
                # Рисуем инвентарь в позиции сущности
                inventory_component.draw_inventory(screen, position_component.x, position_component.y, 200, 200)
