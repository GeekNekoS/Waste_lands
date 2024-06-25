import pygame
from mvc.controller.a_star import AStar
import threading


class Enemy:
    def __init__(self, x: int, y: int, sprite_paths: dict, movement_speed: float = 1):
        self.x = x
        self.y = y
        self.sprites = self.load_sprites(sprite_paths)
        self.direction = 'down'
        self.current_sprite = 0
        self.movement_speed = movement_speed
        self.rect = self.sprites[self.direction][0].get_rect(topleft=(self.x, self.y))
        self.animation_speed = 10
        self.frame_count = 0

        self.path = []
        self.direction_changed = False
        self.target_pos = None
        self.last_path_update_time = 0
        self.path_update_interval = 2000  # 2 seconds
        self.updating_path = False

    def find_path_to_player(self, player_pos, grid):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_path_update_time >= self.path_update_interval or self.target_pos != player_pos:
            if not self.updating_path:
                self.updating_path = True
                threading.Thread(target=self._update_path, args=(player_pos, grid)).start()

    def _update_path(self, player_pos, grid):
        try:
            start = (int(self.x), int(self.y))
            goal = (int(player_pos[0]), int(player_pos[1]))
            astar = AStar(grid)
            path = astar.find_path(start, goal)
            if path:
                self.path = path
            self.target_pos = player_pos
            self.last_path_update_time = pygame.time.get_ticks()
        except Exception as e:
            self.path = []
        finally:
            self.updating_path = False

    def load_sprites(self, sprite_paths: dict) -> dict:
        sprites = {}
        for direction, paths in sprite_paths.items():
            sprites[direction] = [pygame.image.load(path).convert_alpha() for path in paths]
        return sprites

    def update(self, player_rect: pygame.Rect, dt: float, grid: list):
        if not self.path or self.direction_changed or self.target_pos != (player_rect.x, player_rect.y):
            self.find_path_to_player((player_rect.x, player_rect.y), grid)
            self.direction_changed = False

        if self.path:
            try:
                next_node = self.path[0]
                dx, dy = next_node[0] - self.x, next_node[1] - self.y

                step = self.movement_speed * dt
                move_x = min(max(dx, -step), step)
                move_y = min(max(dy, -step), step)

                if abs(dx) < step:
                    move_x = dx
                if abs(dy) < step:
                    move_y = dy

                self.direction = 'right' if dx > 0 else 'left' if dx < 0 else 'down' if dy > 0 else 'up'

                self.update_position(move_x, move_y)

                if (self.x, self.y) == next_node:
                    self.path.pop(0)

            except Exception as e:
                self.path = []

        # Удаляем логику, которая останавливает анимацию при отсутствии пути
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites[self.direction])

    def update_position(self, move_x: float, move_y: float):
        self.x += move_x
        self.y += move_y
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen: pygame.Surface, camera_x: int, camera_y: int, debug: bool = False):
        screen.blit(self.sprites[self.direction][self.current_sprite], (self.x - camera_x, self.y - camera_y))
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self.rect.move(-camera_x, -camera_y), 1)
