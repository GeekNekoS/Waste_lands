import pygame
from config import player_sprites
from settings import debug, WIDTH, HEIGHT


class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos):
        super().__init__()
        # Загрузка спрайтов для всех направлений
        self.sprites = {
            'left': [pygame.image.load(f'{player_sprites}left_{i}.png').convert_alpha() for i in range(1, 5)],
            'right': [pygame.image.load(f'{player_sprites}right_{i}.png').convert_alpha() for i in range(1, 5)],
            'up': [pygame.image.load(f'{player_sprites}up_{i}.png').convert_alpha() for i in range(1, 5)],
            'down': [pygame.image.load(f'{player_sprites}down_{i}.png').convert_alpha() for i in range(1, 5)]
        }
        self.direction = 'down'
        self.current_sprites = self.sprites[self.direction]
        self.current_frame = 0
        self.image = self.current_sprites[self.current_frame]
        self.rect = self.image.get_rect(topleft=start_pos)
        self.movement_speed = 200
        self.animation_speed = 0.1
        self.animation_counter = 0

        # Установка хитбокса
        hitbox_width = self.rect.width // 2
        hitbox_height = self.rect.height // 2
        self.hitbox = pygame.Rect(
            self.rect.x + (self.rect.width - hitbox_width) // 2,
            self.rect.y + (self.rect.height - hitbox_height) // 2,
            hitbox_width,
            hitbox_height
        )

    def update(self, keys, dt, trees):
        self.move(keys, dt, trees)
        if self.is_moving:
            self.animate(dt)
        else:
            self.current_frame = 0
            self.image = self.current_sprites[self.current_frame]

    def animate(self, dt):
        self.animation_counter += dt
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.current_sprites)
            self.image = self.current_sprites[self.current_frame]

    def move(self, keys, dt, trees):
        dx, dy = 0, 0
        moving = False

        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:  # Проверяем, что нажата только клавиша влево
            dx -= self.movement_speed * dt
            if self.direction != 'left':
                self.direction = 'left'
                self.current_sprites = self.sprites['left']
                self.current_frame = 0
            moving = True
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:  # Проверяем, что нажата только клавиша вправо
            dx += self.movement_speed * dt
            if self.direction != 'right':
                self.direction = 'right'
                self.current_sprites = self.sprites['right']
                self.current_frame = 0
            moving = True
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:  # Проверяем, что нажата только клавиша вверх
            dy -= self.movement_speed * dt
            if self.direction != 'up':
                self.direction = 'up'
                self.current_sprites = self.sprites['up']
                self.current_frame = 0
            moving = True
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:  # Проверяем, что нажата только клавиша вниз
            dy += self.movement_speed * dt
            if self.direction != 'down':
                self.direction = 'down'
                self.current_sprites = self.sprites['down']
                self.current_frame = 0
            moving = True

        if moving:
            new_rect = self.rect.move(dx, dy)
            new_hitbox = self.hitbox.move(dx, dy)

            if 0 <= new_hitbox.left and new_hitbox.right <= WIDTH and 0 <= new_hitbox.top and new_hitbox.bottom <= HEIGHT:
                if not any(new_hitbox.colliderect(tree[1]) for tree in trees):
                    self.rect = new_rect
                    self.hitbox = new_hitbox
                    self.is_moving = True
                else:
                    self.is_moving = False
            else:
                self.is_moving = False
        else:
            self.is_moving = False

        self.update_hitbox()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)  # Отрисовка хитбокса красной линией

    def update_hitbox(self):
        # Обновляем хитбокс игрока после его перемещения
        hitbox_width = self.rect.width // 2
        hitbox_height = self.rect.height // 2
        self.hitbox = pygame.Rect(
            self.rect.x + (self.rect.width - hitbox_width) // 2,
            self.rect.y + self.rect.height - hitbox_height,  # Позиция ниже спрайта
            hitbox_width,
            hitbox_height
        )
