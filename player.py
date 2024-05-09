import pygame


class Player:
    def __init__(self, start_pos):
        self.image = pygame.Surface((40, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=start_pos)
        self.speed = 200

    def update(self, keys, dt):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed * dt
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed * dt
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed * dt

    def draw(self, screen):
        screen.blit(self.image, self.rect)
