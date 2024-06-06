import pygame


class Enemy:
    def __init__(self, x, y, sprite_paths, movement_speed=1):
        self.x = x
        self.y = y
        self.sprites = self.load_sprites(sprite_paths)
        self.direction = 'down'  # Начальное направление движения
        self.current_sprite = 0
        self.movement_speed = movement_speed
        self.rect = self.sprites[self.direction][0].get_rect(topleft=(self.x, self.y))
        self.animation_speed = 10  # Скорость анимации (чем больше значение, тем медленнее анимация)
        self.frame_count = 0  # Счетчик кадров

    def load_sprites(self, sprite_paths):
        sprites = {}
        for direction, paths in sprite_paths.items():
            sprites[direction] = [pygame.image.load(path).convert_alpha() for path in paths]
            print(f"Loaded {len(sprites[direction])} sprites for direction '{direction}'")  # Отладочное сообщение
        return sprites

    def update(self, player_rect, dt, enemies):
        move_x, move_y = 0, 0

        # Определяем направление игрока относительно дракона
        if player_rect.x > self.x:
            self.direction = 'right'
        elif player_rect.x < self.x:
            self.direction = 'left'
        if player_rect.y > self.y:
            if abs(player_rect.y - self.y) > abs(player_rect.x - self.x):
                self.direction = 'down'
        elif player_rect.y < self.y:
            if abs(player_rect.y - self.y) > abs(player_rect.x - self.x):
                self.direction = 'up'

        # Перемещаем дракона по оси X в зависимости от направления
        if self.direction == 'right':
            move_x = self.movement_speed * dt
        elif self.direction == 'left':
            move_x = -self.movement_speed * dt
        elif self.direction == 'down':
            move_y = self.movement_speed * dt
        elif self.direction == 'up':
            move_y = -self.movement_speed * dt

        # Сохранение предыдущих координат для отката при столкновении
        prev_x, prev_y = self.x, self.y

        # Перемещение врага
        self.x += move_x
        self.y += move_y

        # Обновление хитбокса
        self.rect.topleft = (self.x, self.y)

        # Проверка столкновений с другими драконами
        for enemy in enemies:
            if enemy != self and self.rect.colliderect(enemy.rect):
                self.x, self.y = prev_x, prev_y
                self.rect.topleft = (self.x, self.y)
                break

        # Обновляем спрайт с учетом скорости анимации
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites[self.direction]):
                self.current_sprite = 0

    def draw(self, screen, camera_x, camera_y, debug=False):
        screen.blit(self.sprites[self.direction][self.current_sprite], (self.x - camera_x, self.y - camera_y))
        if debug:
            # Отрисовка хитбокса
            pygame.draw.rect(screen, (255, 0, 0), self.rect.move(-camera_x, -camera_y), 1)
        print(f"Enemy drawn at position ({self.x - camera_x}, {self.y - camera_y}), direction: {self.direction}, current sprite: {self.current_sprite}")  # Отладочное сообщение
