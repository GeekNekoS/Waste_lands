import pygame
import random


class World:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tree_image = pygame.image.load('objects/tree.jpg')  # Указать правильный путь к файлу
        self.tree_image = pygame.transform.scale(self.tree_image, (150, 150))
        self.trees = []
        self.generate_world()

    def generate_world(self):
        for _ in range(10):  # Создаем 10 деревьев
            self.add_tree()

    def add_tree(self):
        max_attempts = 50
        tree_size = (150, 150)
        while max_attempts > 0:
            x = random.randint(0, self.screen_width - tree_size[0])
            y = random.randint(0, self.screen_height - tree_size[1])
            new_tree_rect = pygame.Rect(x, y, *tree_size)
            if not any(tree.colliderect(new_tree_rect) for tree in self.trees):
                self.trees.append(new_tree_rect)
                break
            max_attempts -= 1

    def draw(self, screen):
        for tree_rect in self.trees:
            screen.blit(self.tree_image, tree_rect)
