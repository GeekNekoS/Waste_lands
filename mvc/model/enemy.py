import pygame
from mvc.controller.a_star import AStar
import threading


class Enemy:
    def __init__(self, x: int, y: int, sprite_paths: dict, movement_speed: float = 2):
        self.x = x
        self.y = y
        self.sprites = self.load_sprites(sprite_paths)
        self.direction = 'down'
        self.current_sprite = 0
        self.movement_speed = movement_speed
        self.rect = self.sprites[self.direction][0].get_rect(topleft=(self.x, self.y))
        self.animation_speed = 150  # 150 миллисекунд
        self.last_animation_update_time = pygame.time.get_ticks()

        self.path = []
        self.direction_changed = False
        self.target_pos = None
        self.last_path_update_time = 0
        self.path_update_interval = 2000  # 2000 миллисекунд
        self.updating_path = False

    def find_path_to_player(self, player_pos, grid):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_path_update_time >= self.path_update_interval:
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
        # Проверяем и обновляем путь, если прошло достаточно времени или пути нет
        if not self.path or pygame.time.get_ticks() - self.last_path_update_time >= self.path_update_interval:
            self.find_path_to_player((player_rect.x, player_rect.y), grid)

        if self.path:
            try:
                next_node = self.path[0]
                dx, dy = next_node[0] - self.x, next_node[1] - self.y

                # Увеличиваем шаг перемещения
                step = self.movement_speed * dt * 2  # Увеличено в 2 раза
                move_x = min(max(dx, -step), step)
                move_y = min(max(dy, -step), step)

                # Проверяем значительные изменения в направлении
                if abs(dx) > 0.1 or abs(dy) > 0.1:
                    if abs(dx) > abs(dy):
                        self.direction = 'right' if dx > 0 else 'left'
                    else:
                        self.direction = 'down' if dy > 0 else 'up'

                self.update_position(move_x, move_y)

                # Если достигли следующего узла, удаляем его из пути
                if (self.x, self.y) == next_node:
                    self.path.pop(0)

            except Exception as e:
                self.path = []

        # Обновляем анимацию по времени, а не по кадрам
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_update_time >= self.animation_speed:
            self.last_animation_update_time = current_time
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites[self.direction])

    def update_position(self, move_x: float, move_y: float):
        self.x += move_x
        self.y += move_y
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen: pygame.Surface, camera_x: int, camera_y: int, debug: bool = False):
        screen.blit(self.sprites[self.direction][self.current_sprite], (self.x - camera_x, self.y - camera_y))
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self.rect.move(-camera_x, -camera_y), 1)
