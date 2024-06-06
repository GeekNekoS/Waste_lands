import pygame
import random
import numpy as np
from settings import debug, WIDTH, HEIGHT
from mvc.model.inventory import Inventory, InventoryPanel
from mvc.model.items import Axe
from mvc.controller.utils import detect_item_pickup, draw_debug_line_to_tree, distance
from mvc.controller.perlin_noise import perlin, generate_permutation_table
from mvc.model.enemy import Enemy


class World:
    def __init__(self):
        self.tree_image = pygame.image.load('sprites/tree.png').convert_alpha()
        self.tree_image = pygame.transform.scale(self.tree_image, (150, 150))
        self.trees = []
        self.enemies = []
        self.visibility_radius = 200  # Радиус области видимости перед игроком

        # Переменные для шума Перлина
        self.width = WIDTH // 32  # Размеры карты в "клетках" (32x32 пикселей)
        self.height = HEIGHT // 32
        self.scale = 10
        self.permutation = generate_permutation_table(seed=42)

        self.generate_terrain()
        self.enemies = self.generate_enemies()  # Генерация врагов
        self.camera_x = 0
        self.camera_y = 0

        # Создаем панель инвентаря для персонажа
        self.player_inventory = Inventory(max_slots=4)
        panel_width = 200  # Ширина панели инвентаря
        panel_height = 50  # Высота панели инвентаря
        panel_x = (WIDTH - panel_width) // 2  # Рассчитываем координату x для центрирования панели по горизонтали
        panel_y = 10  # Размещаем панель в самом верху экрана
        self.inventory_panel = InventoryPanel(x=panel_x, y=panel_y, width=panel_width, height=panel_height,
                                              inventory=self.player_inventory)

        self.axe = Axe()  # Создаем экземпляр класса Axe
        self.axe_rect = pygame.Rect(0, 0, self.axe.icon.get_width(), self.axe.icon.get_height())
        self.spawn_axe()

        # Определяем флаг для отслеживания подбора предмета в текущем кадре
        self.item_picked_up_this_frame = False

    def generate_enemies(self):
        enemies = []
        sprite_paths = {
            'up': ['sprites/dragon/up_1.png', 'sprites/dragon/up_2.png', 'sprites/dragon/up_3.png', 'sprites/dragon/up_4.png'],
            'down': ['sprites/dragon/down_1.png', 'sprites/dragon/down_2.png', 'sprites/dragon/down_3.png', 'sprites/dragon/down_4.png'],
            'left': ['sprites/dragon/left_1.png', 'sprites/dragon/left_2.png', 'sprites/dragon/left_3.png', 'sprites/dragon/left_4.png'],
            'right': ['sprites/dragon/right_1.png', 'sprites/dragon/right_2.png', 'sprites/dragon/right_3.png', 'sprites/dragon/right_4.png']
        }
        for _ in range(5):
            x = random.randint(0, WIDTH * 3)
            y = random.randint(0, HEIGHT * 3)
            enemies.append(Enemy(x, y, sprite_paths, movement_speed=20))
        return enemies

    def spawn_axe(self):
        # Переменная для хранения коллизий с деревьями
        tree_collisions = [tree[0].inflate(20, 20) for tree in self.trees]

        while True:
            # Случайные координаты для топора
            x = random.randint(0, WIDTH - self.axe.icon.get_width())
            y = random.randint(0, HEIGHT - self.axe.icon.get_height())

            # Создаем прямоугольник для проверки коллизий
            axe_rect = pygame.Rect(x, y, self.axe.icon.get_width(), self.axe.icon.get_height())

            # Проверяем, не пересекается ли топор с деревьями
            intersects_trees = any(axe_rect.colliderect(tree) for tree in tree_collisions)

            # Если топор не пересекается с деревьями, выходим из цикла
            if not intersects_trees:
                break

        # Устанавливаем координаты для топора
        self.axe_rect.x = x
        self.axe_rect.y = y

    def generate_terrain(self):
        noise_map = self.generate_perlin_noise(self.width, self.height, self.scale)
        tree_threshold = 0.1  # Пороговое значение для размещения деревьев
        min_distance_between_trees = 100  # Минимальное расстояние между деревьями

        # Список для хранения координат существующих деревьев
        existing_tree_positions = []

        for x in range(self.width):
            for y in range(self.height):
                if noise_map[x][y] > tree_threshold:
                    attempts = 0
                    while attempts < 10:  # Ограничиваем число попыток, чтобы избежать бесконечного цикла
                        new_x = x * 32 + random.randint(-50, 50)  # Генерируем случайное смещение относительно клетки
                        new_y = y * 32 + random.randint(-50, 50)
                        if self.is_far_enough_from_existing_trees(existing_tree_positions, new_x, new_y,
                                                                  min_distance_between_trees):
                            self.add_tree(new_x, new_y)
                            existing_tree_positions.append((new_x, new_y))  # Добавляем новое дерево в список
                            break
                        attempts += 1

    def is_far_enough_from_existing_trees(self, existing_tree_positions, x, y, min_distance):
        for tree_x, tree_y in existing_tree_positions:
            distance = ((x - tree_x) ** 2 + (y - tree_y) ** 2) ** 0.5
            if distance < min_distance:
                return False
        return True

    def generate_perlin_noise(self, width, height, scale):
        shape = (width, height)
        world = np.zeros(shape)
        for i in range(shape[0]):
            for j in range(shape[1]):
                x = i / scale
                y = j / scale
                world[i][j] = perlin(x, y, self.permutation)
                if debug:
                    print(f"Noise value at ({i}, {j}): {world[i][j]}")
        return world

    def add_tree(self, x=None, y=None):
        max_attempts = 50
        image_size = (150, 150)
        hitbox_size = (30, 30)
        if x is None or y is None:
            while max_attempts > 0:
                x = random.randint(0, WIDTH - image_size[0])
                y = random.randint(0, HEIGHT - image_size[1])
                image_rect = pygame.Rect(x, y, *image_size)
                hitbox_x = x + (image_size[0] - hitbox_size[0]) // 2
                hitbox_y = y + image_size[1] - hitbox_size[1] - 10
                hitbox_rect = pygame.Rect(hitbox_x, hitbox_y, *hitbox_size)
                if not any(tree[1].colliderect(hitbox_rect) for tree in self.trees):
                    self.trees.append((image_rect, hitbox_rect))
                    if debug:
                        print(f"Tree added randomly at ({x}, {y})")
                    break
                max_attempts -= 1
        else:
            image_rect = pygame.Rect(x, y, *image_size)
            hitbox_x = x + (image_size[0] - hitbox_size[0]) // 2
            hitbox_y = y + image_size[1] - hitbox_size[1] - 10
            hitbox_rect = pygame.Rect(hitbox_x, hitbox_y, *hitbox_size)
            self.trees.append((image_rect, hitbox_rect))
            if debug:
                print(f"Tree added at ({x}, {y})")

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

        # Затемняем весь экран
        darkness_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        darkness_surface.fill((0, 0, 0, 150))  # Черный цвет с непрозрачностью

        # Создаем поверхность для затемнения объектов
        object_darkness_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        object_darkness_surface.fill((0, 0, 0, 100))  # Черный цвет с непрозрачностью

        # Отрисовываем затемнение на экране
        screen.blit(darkness_surface, (0, 0))

        # Рисуем топор
        screen.blit(self.axe.icon, self.axe_rect.move(-camera_x, -camera_y))

        # Рассчитываем область видимости вокруг игрока
        visibility_radius = self.visibility_radius
        visibility_area = pygame.Rect(player.rect.centerx - visibility_radius,
                                      player.rect.centery - visibility_radius,
                                      2 * visibility_radius, 2 * visibility_radius)

        # Рисуем круг области видимости на поверхности затемнения
        player_hitbox_center = (player.hitbox.centerx - camera_x, player.hitbox.centery - camera_y)
        pygame.draw.circle(darkness_surface, (0, 0, 0, 0), player_hitbox_center, self.visibility_radius)

        # Отрисовываем деревья, находящиеся ниже персонажа
        for image_rect, hitbox_rect in self.trees:
            if player.rect.bottom > hitbox_rect.top:
                draw_rect = image_rect.move(-camera_x, -camera_y)
                screen.blit(self.tree_image, draw_rect)
                if debug:
                    draw_hitbox = hitbox_rect.move(-camera_x, -camera_y)
                    pygame.draw.rect(screen, (255, 0, 0), draw_hitbox, 1)  # отрисовка хитбокса объекта для отладки

        # Отрисовываем персонажа
        player.draw(screen, camera_x, camera_y)

        # Отрисовываем деревья, находящиеся выше персонажа
        for image_rect, hitbox_rect in self.trees:
            if player.rect.bottom <= hitbox_rect.top:
                draw_rect = image_rect.move(-camera_x, -camera_y)
                screen.blit(self.tree_image, draw_rect)
                if debug:
                    draw_hitbox = hitbox_rect.move(-camera_x, -camera_y)
                    pygame.draw.rect(screen, (255, 0, 0), draw_hitbox, 2)  # отрисовка хитбокса объекта для отладки

        # Рисуем затемнение на экране
        screen.blit(darkness_surface, (0, 0))

        # Рисуем предмет только если он находится в области видимости и не пересекается с деревьями
        if visibility_area.colliderect(self.axe_rect.move(-camera_x, -camera_y)):
            axe_visible = True
            for image_rect, hitbox_rect in self.trees:
                if self.axe_rect.colliderect(hitbox_rect):
                    axe_visible = False
                    break
            if axe_visible:
                screen.blit(self.axe.icon, self.axe_rect.move(-camera_x, -camera_y))

        # Отрисовываем панель инвентаря
        self.inventory_panel.draw(screen)

        # Рисуем красную линию окружности в режиме отладки
        if debug:
            pygame.draw.circle(screen, (255, 0, 0), player_hitbox_center, self.visibility_radius, 1)

            # Если включен режим отладки, рисуем линию от игрока до предмета
            item_center = (self.axe_rect.centerx - camera_x, self.axe_rect.centery - camera_y)
            pygame.draw.line(screen, (255, 0, 0), player_hitbox_center, item_center)

            # Рисуем линию от игрока до ближайшего дерева
            draw_debug_line_to_tree(screen, player.rect, self.trees, camera_x, camera_y)

        # Применяем затемнение к предмету
        screen.blit(object_darkness_surface, (0, 0))

        # Отрисовываем врагов
        for enemy in self.enemies:
            print(f"Рисуем врага на позиции ({enemy.x}, {enemy.y})")  # Отладочное сообщение
            enemy.draw(screen, camera_x, camera_y)

    def add_item_to_player_inventory(self, item):
        # Проверяем, есть ли свободное место в инвентаре
        if len(self.player_inventory) < self.player_inventory.max_slots:
            # Добавляем предмет в инвентарь
            success = self.player_inventory.add_item(item)
            if success:
                print("Предмет добавлен в инвентарь персонажа.")
                # Обновляем панель инвентаря после добавления предмета
                self.inventory_panel.update_inventory(self.player_inventory)
            return success
        else:
            return False

    def update(self, player_rect, dt):
        # Проверяем, подобран ли предмет и нажата ли клавиша "E"
        if detect_item_pickup(player_rect, self.axe_rect) and pygame.key.get_pressed()[pygame.K_e]:
            # Проверяем, не подбирался ли предмет уже в текущем кадре
            if not self.item_picked_up_this_frame:
                # Устанавливаем флаг в True, чтобы пометить, что предмет подобран в этом кадре
                self.item_picked_up_this_frame = True
                # Проверяем, не полон ли инвентарь игрока
                if len(self.player_inventory) >= self.player_inventory.max_slots:
                    print("Инвентарь персонажа полон, предмет не подобран.")
                else:
                    # Добавляем топор в инвентарь
                    self.add_item_to_player_inventory(self.axe)
        else:
            # Сбрасываем флаг, если предмет не был подобран в текущем кадре
            self.item_picked_up_this_frame = False

        # Обновление врагов
        for enemy in self.enemies:
            print(f"Обновляем врага на позиции ({enemy.x}, {enemy.y})")  # Отладочное сообщение
            enemy.update(player_rect, dt)
