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
        self.target_pos = None  # Добавлено для отслеживания позиции игрока

    def find_path_to_player(self, player_pos):
        try:
            start = (int(self.x), int(self.y))
            goal = (int(player_pos[0]), int(player_pos[1]))
            astar = AStar(self.grid_width, self.grid_height)
            self.path = astar.find_path(start, goal)
            # print(f"Path found: {self.path}")
        except Exception as e:
            # print(f"Error finding path: {e}")
            pass

    def load_sprites(self, sprite_paths):
        sprites = {}
        for direction, paths in sprite_paths.items():
            sprites[direction] = [pygame.image.load(path).convert_alpha() for path in paths]
        return sprites

    def update(self, player_rect, dt, enemies):
        move_x, move_y = 0, 0

        if not self.path or self.direction_changed or self.target_pos != (player_rect.x, player_rect.y):
            print(
                f"Updating path for enemy at ({self.x}, {self.y}) towards player at ({player_rect.x}, {player_rect.y})")
            self.find_path_to_player((player_rect.x, player_rect.y))
            self.direction_changed = False
            self.target_pos = (player_rect.x, player_rect.y)

        if self.path:
            try:
                next_node = self.path[0]
                dx, dy = next_node[0] - self.x, next_node[1] - self.y
                print(f"Next node: {next_node}, current position: ({self.x}, {self.y}), delta: ({dx}, {dy})")

                if dx != 0:
                    move_x = self.movement_speed * dt if dx > 0 else -self.movement_speed * dt
                if dy != 0:
                    move_y = self.movement_speed * dt if dy > 0 else -self.movement_speed * dt

                prev_x, prev_y = self.x, self.y

                direction_before = self.direction
                if abs(dx) > abs(dy):
                    self.direction = 'right' if dx > 0 else 'left'
                else:
                    self.direction = 'down' if dy > 0 else 'up'

                if self.direction != direction_before:
                    self.direction_changed = True

                self.update_position(move_x, move_y)
                print(f"Moved to: ({self.x}, {self.y}), move: ({move_x}, {move_y})")

                if self.check_collisions(enemies):
                    print("Collision detected, reverting position.")
                    self.x, self.y = prev_x, prev_y
                    self.rect.topleft = (self.x, self.y)
                else:
                    if abs(self.x - next_node[0]) < self.movement_speed * dt and abs(
                            self.y - next_node[1]) < self.movement_speed * dt:
                        self.x, self.y = next_node
                        self.path.pop(0)
                        print(f"Reached node: {next_node}, updated path: {self.path}")

            except Exception as e:
                print(f"Error in path update: {e}")
                self.path = []

        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites[self.direction]):
                self.current_sprite = 0

        print(
            f"Dragon position: ({self.x}, {self.y}), direction: {self.direction}, next_node: {next_node if self.path else 'N/A'}, move: ({move_x}, {move_y})")

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
