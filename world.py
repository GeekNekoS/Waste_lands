import pygame
import random
from settings import debug, WIDTH, HEIGHT


class World:
    def __init__(self):
        self.tree_image = pygame.image.load('sprites/tree.png').convert_alpha()
        self.tree_image = pygame.transform.scale(self.tree_image, (150, 150))
        self.trees = []
        for _ in range(10):
            self.add_tree()

    def add_tree(self):
        max_attempts = 50
        image_size = (150, 150)
        hitbox_size = (50, 50)
        while max_attempts > 0:
            x = random.randint(0, WIDTH - image_size[0])
            y = random.randint(0, HEIGHT - image_size[1])
            image_rect = pygame.Rect(x, y, *image_size)
            hitbox_x = x + (image_size[0] - hitbox_size[0]) // 2
            hitbox_y = y + image_size[1] - hitbox_size[1]
            hitbox_rect = pygame.Rect(hitbox_x, hitbox_y, *hitbox_size)
            if not any(tree[1].colliderect(hitbox_rect) for tree in self.trees):
                self.trees.append((image_rect, hitbox_rect))
                break
            max_attempts -= 1

    def draw(self, screen, player):
        # Отрисовываем сначала те деревья, перед которыми персонаж должен находиться
        for image_rect, hitbox_rect in self.trees:
            if player.rect.bottom > hitbox_rect.top:
                screen.blit(self.tree_image, image_rect)
                if debug:
                    pygame.draw.rect(screen, (255, 0, 0), hitbox_rect, 2)  # отрисовка хитбокса дерева для отладки

        # Отрисовка персонажа
        player.draw(screen)

        # Отрисовка деревьев, за которыми должен находиться персонаж
        for image_rect, hitbox_rect in self.trees:
            if player.rect.bottom <= hitbox_rect.top:
                screen.blit(self.tree_image, image_rect)
                if debug:
                    pygame.draw.rect(screen, (255, 0, 0), hitbox_rect, 2)  # отрисовка хитбокса дерева для отладки
