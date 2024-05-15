from components import PositionComponent, VelocityComponent, RenderComponent
import pygame


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
