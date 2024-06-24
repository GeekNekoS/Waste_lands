import pygame
from mvc.controller.a_star import AStar


class Enemy:
    def __init__(self, x, y, sprite_paths, grid_width, grid_height, movement_speed=1):
        self.x = x
        self.y = y
        self.grid_width = grid_width
        self.grid_height = grid_height
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

    def find_path_to_player(self, player_pos):
        try:
            current_time = pygame.time.get_ticks()
            if (current_time - self.last_path_update_time < self.path_update_interval and
                self.target_pos == player_pos):
                return

            start_x = max(0, min(self.grid_width - 1, int(self.x)))
            start_y = max(0, min(self.grid_height - 1, int(self.y)))
            start = (start_x, start_y)

            goal = (int(player_pos[0]), int(player_pos[1]))
            astar = AStar(self.grid_width, self.grid_height)
            self.path = astar.find_path(start, goal)
            self.target_pos = player_pos
            self.last_path_update_time = current_time
            # print(f"Path found: {self.path}")
        except Exception as e:
            # print(f"Error finding path: {e}")
            self.path = []

    def load_sprites(self, sprite_paths):
        sprites = {}
        for direction, paths in sprite_paths.items():
            sprites[direction] = [pygame.image.load(path).convert_alpha() for path in paths]
        return sprites

    def update(self, player_rect, dt, enemies):
        move_x, move_y = 0, 0

        if not self.path or self.direction_changed or self.target_pos != (player_rect.x, player_rect.y):
            self.find_path_to_player((player_rect.x, player_rect.y))
            self.direction_changed = False

        if self.path:
            try:
                next_node = self.path[0]
                dx, dy = next_node[0] - self.x, next_node[1] - self.y
                # print(f"Next node: {next_node}, current position: ({self.x}, {self.y}), delta: ({dx}, {dy})")

                move_x = self.movement_speed * dt if dx > 0 else -self.movement_speed * dt
                move_y = self.movement_speed * dt if dy > 0 else -self.movement_speed * dt

                prev_x, prev_y = self.x, self.y

                self.direction = 'right' if dx > 0 else 'left' if dx < 0 else 'down' if dy > 0 else 'up'

                self.update_position(move_x, move_y)
                # print(f"Moved to: ({self.x}, {self.y}), move: ({move_x}, {move_y})")

                if self.check_collisions(enemies):
                    # print("Collision detected, reverting position.")
                    self.x, self.y = prev_x, prev_y
                    self.rect.topleft = (self.x, self.y)
                elif abs(self.x - next_node[0]) < self.movement_speed * dt and abs(self.y - next_node[1]) < self.movement_speed * dt:
                    self.x, self.y = next_node
                    self.path.pop(0)
                    # print(f"Reached node: {next_node}, updated path: {self.path}")

            except Exception as e:
                # print(f"Error in path update: {e}")
                self.path = []

        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites[self.direction])

        # print(f"Dragon position: ({self.x}, {self.y}), direction: {self.direction}, next_node: {next_node if self.path else 'N/A'}, move: ({move_x}, {move_y})")

    def update_position(self, move_x, move_y):
        self.x += move_x
        self.y += move_y
        self.rect.topleft = (self.x, self.y)

    def check_collisions(self, enemies):
        for enemy in enemies:
            if enemy != self and self.rect.colliderect(enemy.rect):
                return True
        return False

    def draw(self, screen, camera_x, camera_y, debug=False):
        screen.blit(self.sprites[self.direction][self.current_sprite], (self.x - camera_x, self.y - camera_y))
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self.rect.move(-camera_x, -camera_y), 1)
