import pygame
from settings import debug
from components import PositionComponent, HitboxComponent


def draw_debug_line(screen, start_entity, end_entity):
    if not debug:
        return

    start_position = start_entity.get_component(PositionComponent)
    start_hitbox = start_entity.get_component(HitboxComponent)
    start_x = start_position.x + start_hitbox.offset_x + start_hitbox.width / 2
    start_y = start_position.y + start_hitbox.offset_y + start_hitbox.height / 2

    end_position = end_entity.get_component(PositionComponent)
    end_hitbox = end_entity.get_component(HitboxComponent)
    end_x = end_position.x + end_hitbox.offset_x + end_hitbox.width / 2
    end_y = end_position.y + end_hitbox.offset_y + end_hitbox.height / 2

    pygame.draw.line(screen, (0, 255, 255), (start_x, start_y), (end_x, end_y), 2)
