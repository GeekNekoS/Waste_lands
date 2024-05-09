import pygame
from config import player_sprites
from settings import debug


class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos):
        super().__init__()
        self.sprites = {
            'left': [pygame.image.load(f'{player_sprites}left_{i}.png').convert_alpha() for i in range(1, 5)],
            'right': [pygame.image.load(f'{player_sprites}right_{i}.png').convert_alpha() for i in range(1, 5)],
            'up': [pygame.image.load(f'{player_sprites}up_{i}.png').convert_alpha() for i in range(1, 5)],
            'down': [pygame.image.load(f'{player_sprites}down_{i}.png').convert_alpha() for i in range(1, 5)]
        }
        self.current_sprites = self.sprites['down']
        self.current_frame = 0
        self.image = self.current_sprites[self.current_frame]
        self.rect = self.image.get_rect(topleft=start_pos)
        self.movement_speed = 200
        self.direction = 'down'
        self.animation_speed = 0.1
        self.animation_counter = 0

        # Уменьшаем хитбокс игрока
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

    def animate(self, dt):
        self.animation_counter += dt
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.current_sprites)
            self.image = self.current_sprites[self.current_frame]

    def move(self, keys, dt, trees):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx -= self.movement_speed * dt
            self.direction = 'left'
        if keys[pygame.K_RIGHT]:
            dx += self.movement_speed * dt
            self.direction = 'right'
        if keys[pygame.K_UP]:
            dy -= self.movement_speed * dt
            self.direction = 'up'
        if keys[pygame.K_DOWN]:
            dy += self.movement_speed * dt
            self.direction = 'down'

        new_rect = self.rect.move(dx, dy)
        new_hitbox = self.hitbox.move(dx, dy)
        if not any(new_hitbox.colliderect(tree[1]) for tree in trees):
            self.rect = new_rect
            self.hitbox = new_hitbox
            self.is_moving = True
        else:
            self.is_moving = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)  # Отрисовка хитбокса красной линией
