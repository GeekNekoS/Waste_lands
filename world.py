import pygame
import random


class World:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        original_tree_image = pygame.image.load('objects/tree_removebg.png')  # Путь к вашему изображению дерева
        self.tree_image = pygame.transform.scale(original_tree_image, (150, 150))  # Масштабирование изображения до нового размера
        self.trees = []  # Список прямоугольников, представляющих деревья
        self.generate_world()

    def generate_world(self):
        tree_count = 10
        for _ in range(tree_count):
            self.add_tree()

    def add_tree(self):
        max_attempts = 50  # Максимальное количество попыток для поиска свободного места
        tree_size = (125, 125)  # Размер каждого дерева
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

    def update(self, dt):
        # В этом примере обновление мира не зависит от dt, но структура готова для будущих изменений
        pass
