import pygame
from mvc.controller.a_star import AStar


class Enemy:
    def __init__(self, x, y, sprite_paths, movement_speed=1):
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
        self.path_update_interval = 2000  # Изменим интервал обновления пути до 2 секунд

    def find_path_to_player(self, player_pos, grid):
        try:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_path_update_time >= self.path_update_interval or self.target_pos != player_pos:
                start = (int(self.x), int(self.y))
                goal = (int(player_pos[0]), int(player_pos[1]))
                astar = AStar(grid)
                self.path = astar.find_path(start, goal)
                self.target_pos = player_pos
                self.last_path_update_time = current_time

        except Exception as e:
            self.path = []

    def load_sprites(self, sprite_paths):
        sprites = {}
        for direction, paths in sprite_paths.items():
            sprites[direction] = [pygame.image.load(path).convert_alpha() for path in paths]
        return sprites

    def update(self, player_rect, dt, grid):
        move_x, move_y = 0, 0

        if not self.path or self.direction_changed or self.target_pos != (player_rect.x, player_rect.y):
            self.find_path_to_player((player_rect.x, player_rect.y), grid)
            self.direction_changed = False

        if self.path:
            try:
                next_node = self.path[0]
                dx, dy = next_node[0] - self.x, next_node[1] - self.y

                step = self.movement_speed * dt
                move_x = step if dx > 0 else -step
                move_y = step if dy > 0 else -step

                prev_x, prev_y = self.x, self.y

                self.direction = 'right' if dx > 0 else 'left' if dx < 0 else 'down' if dy > 0 else 'up'

                self.update_position(move_x, move_y)
                self.x = round(self.x)
                self.y = round(self.y)
                self.rect.topleft = (self.x, self.y)

                if abs(self.x - next_node[0]) < step and abs(self.y - next_node[1]) < step:
                    self.x, self.y = next_node
                    self.path.pop(0)

            except Exception as e:
                self.path = []

        if not self.path:
            self.frame_count = 0

        if not self.direction_changed:
            self.frame_count += 1
            if self.frame_count >= self.animation_speed:
                self.frame_count = 0
                self.current_sprite = (self.current_sprite + 1) % len(self.sprites[self.direction])

    def update_position(self, move_x, move_y):
        self.x += move_x
        self.y += move_y
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen, camera_x, camera_y, debug=False):
        screen.blit(self.sprites[self.direction][self.current_sprite], (self.x - camera_x, self.y - camera_y))
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self.rect.move(-camera_x, -camera_y), 1)
