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

    def update(self, player_rect, dt):
        move_x, move_y = 0, 0

        # Определяем направление игрока относительно дракона
        if player_rect.x > self.x:
            self.direction = 'right'
        elif player_rect.x < self.x:
            self.direction = 'left'

        # Перемещаем дракона по оси X в зависимости от направления
        if self.direction == 'right':
            move_x = self.movement_speed * dt
        elif self.direction == 'left':
            move_x = -self.movement_speed * dt

        # Перемещаем дракона по оси Y
        if player_rect.y > self.y:
            move_y = self.movement_speed * dt
        elif player_rect.y < self.y:
            move_y = -self.movement_speed * dt

        # Перемещение врага
        self.x += move_x
        self.y += move_y

        # Обновляем спрайт с учетом скорости анимации
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites[self.direction]):
                self.current_sprite = 0

        self.rect.topleft = (self.x, self.y)

    def draw(self, screen, camera_x, camera_y):
        sprite = self.sprites[self.direction][self.current_sprite]  # Выбираем спрайт в зависимости от направления
        screen.blit(sprite, (self.x - camera_x, self.y - camera_y))
        print(f"Enemy drawn at position ({self.x - camera_x}, {self.y - camera_y}), direction: {self.direction}, current sprite: {self.current_sprite}")  # Отладочное сообщение
