import pygame
import random
from settings import debug, WIDTH, HEIGHT


class World:
    def __init__(self):
        self.tree_image = pygame.image.load('sprites/tree.png').convert_alpha()
        self.tree_image = pygame.transform.scale(self.tree_image, (150, 150))
        self.trees = []
        self.visibility_radius = 200  # Радиус области видимости перед игроком
        for _ in range(15):
            self.add_tree()
        self.camera_x = 0
        self.camera_y = 0

    def add_tree(self):
        max_attempts = 50
        image_size = (150, 150)
        hitbox_size = (30, 30)
        while max_attempts > 0:
            x = random.randint(0, WIDTH - image_size[0])
            y = random.randint(0, HEIGHT - image_size[1])
            image_rect = pygame.Rect(x, y, *image_size)
            hitbox_x = x + (image_size[0] - hitbox_size[0]) // 2
            hitbox_y = y + image_size[1] - hitbox_size[1] - 10
            hitbox_rect = pygame.Rect(hitbox_x, hitbox_y, *hitbox_size)
            if not any(tree[1].colliderect(hitbox_rect) for tree in self.trees):
                self.trees.append((image_rect, hitbox_rect))
                break
            max_attempts -= 1

    def get_save_data(self):
        return [(tree[1].x, tree[1].y) for tree in self.trees]

    def load_from_save(self, tree_positions):
        self.trees = []
        for pos in tree_positions:
            image_size = (150, 150)
            hitbox_size = (50, 50)
            image_rect = pygame.Rect(pos[0], pos[1], *image_size)
            hitbox_x = pos[0] + (image_size[0] - hitbox_size[0]) // 2
            hitbox_y = pos[1] + image_size[1] - hitbox_size[1]
            hitbox_rect = pygame.Rect(hitbox_x, hitbox_y, *hitbox_size)
            self.trees.append((image_rect, hitbox_rect))

    def draw(self, screen, player, camera_x, camera_y):
        # Рассчитываем смещение камеры, чтобы персонаж оказался по центру экрана по горизонтали
        player_center_x = player.rect.centerx
        camera_center_x = WIDTH // 2  # Центр экрана по горизонтали
        camera_x = player_center_x - camera_center_x

        # Рассчитываем область видимости вокруг игрока
        visibility_radius = self.visibility_radius
        visibility_area = pygame.Rect(player.rect.centerx - visibility_radius,
                                      player.rect.centery - visibility_radius,
                                      2 * visibility_radius, 2 * visibility_radius)

        # Затемняем весь экран
        screen.fill((0, 0, 0))

        # Создаем поверхность для затемнения
        darkness_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        darkness_surface.fill((0, 0, 0, 100))  # Черный цвет с непрозрачностью

        # Рисуем круг области видимости на поверхности затемнения
        player_hitbox_center = (player.hitbox.centerx - camera_x, player.hitbox.centery - camera_y)
        pygame.draw.circle(darkness_surface, (0, 0, 0, 0), player_hitbox_center, self.visibility_radius)

        # Отрисовываем объекты в пределах области видимости
        for image_rect, hitbox_rect in self.trees:
            if visibility_area.colliderect(image_rect):
                draw_rect = image_rect.move(-camera_x, -camera_y)
                screen.blit(self.tree_image, draw_rect)
                if debug:
                    draw_hitbox = hitbox_rect.move(-camera_x, -camera_y)
                    pygame.draw.rect(screen, (255, 0, 0), draw_hitbox, 2)  # отрисовка хитбокса объекта для отладки

        # Отрисовываем персонажа
        player.draw(screen, camera_x, camera_y)

        # Рисуем затемнение на экране
        screen.blit(darkness_surface, (0, 0))

        # Рисуем красную линию окружности в режиме отладки
        if debug:
            pygame.draw.circle(screen, (255, 0, 0), player_hitbox_center, self.visibility_radius, 1)
