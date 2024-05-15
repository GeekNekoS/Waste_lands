import pygame
import random
from settings import debug, WIDTH, HEIGHT
from old_files_darft.inventory import Inventory, InventoryPanel
from old_files_darft.items import Axe
from old_files_darft.utils import detect_item_pickup


class World:
    def __init__(self):
        self.tree_image = pygame.image.load('../sprites/tree.png').convert_alpha()
        self.tree_image = pygame.transform.scale(self.tree_image, (150, 150))
        self.trees = []
        self.visibility_radius = 200  # Радиус области видимости перед игроком
        for _ in range(15):
            self.add_tree()
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

        # Применяем затемнение к предмету
        screen.blit(object_darkness_surface, (0, 0))

    def add_item_to_player_inventory(self, item):
        # Проверяем, есть ли свободное место в инвентаре
        if len(self.player_inventory) < self.player_inventory.max_slots:
            # Добавляем предмет в инвентарь
            success = self.player_inventory.add_item(item)
            if success:
                print("Предмет добавлен в инвентарь персонажа.")
                # Обновляем панель инвентаря после добавления предмета
                self.inventory_panel.update_inventory(self.player_inventory)
            else:
                print("Инвентарь персонажа полон, предмет не добавлен.")
            return success
        else:
            print("Инвентарь персонажа полон, предмет не добавлен.")
            return False

    def update(self, player_rect):
        if detect_item_pickup(player_rect, self.axe_rect, self.player_inventory, self.axe):
            if len(self.player_inventory) < self.player_inventory.max_slots:  # Проверяем, не полон ли инвентарь
                self.add_item_to_player_inventory(self.axe)  # Добавление предмета в инвентарь
            else:
                print("Инвентарь персонажа полон, предмет не подобран.")
