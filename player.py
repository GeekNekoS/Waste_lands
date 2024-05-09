import pygame


class Player:
    def __init__(self, start_pos):
        self.image = pygame.Surface((40, 50))
        self.image.fill((255, 0, 0))  # Цвет игрока для наглядности
        self.rect = self.image.get_rect(topleft=start_pos)
        self.speed = 200

    def update(self, dt, world):
        keys = pygame.key.get_pressed()
        movement = [0, 0]
        if keys[pygame.K_LEFT]:
            movement[0] -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            movement[0] += self.speed * dt
        if keys[pygame.K_UP]:
            movement[1] -= self.speed * dt
        if keys[pygame.K_DOWN]:
            movement[1] += self.speed * dt

        self.rect.x += movement[0]
        self.rect.y += movement[1]
        self.check_collisions(world)

    def check_collisions(self, world):
        for tree_rect in world.tiles:
            if self.rect.colliderect(tree_rect):
                print("Собрана древесина!")
                world.tiles.remove(tree_rect)  # Удаление дерева после "сбора"
                break  # Выход, чтобы избежать изменения размера списка во время итерации

    def draw(self, screen):
        screen.blit(self.image, self.rect)
