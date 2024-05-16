import random
import pygame
from components import (
    PositionComponent,
    VelocityComponent,
    RenderComponent,
    InventoryComponent,
    AnimationComponent,
    FootstepsComponent,
    HitboxComponent,
    MenuComponent,
    TreeComponent,
    AxeComponent
)
from quadtree import QuadTree
from settings import WIDTH, HEIGHT


class Entity:
    def __init__(self):
        self.components = {}

    def add_component(self, component):
        self.components[type(component)] = component

    def get_component(self, component_type):
        return self.components.get(component_type, None)


def create_player():
    player = Entity()
    player.add_component(PositionComponent(100, 100))
    player.add_component(VelocityComponent(0, 0))
    player.add_component(InventoryComponent(4))

    # Загрузка спрайтов для анимации движения в разные стороны
    down_sprites = [pygame.image.load(f'sprites/player/down_{i}.png') for i in range(1, 5)]
    up_sprites = [pygame.image.load(f'sprites/player/up_{i}.png') for i in range(1, 5)]
    left_sprites = [pygame.image.load(f'sprites/player/left_{i}.png') for i in range(1, 5)]
    right_sprites = [pygame.image.load(f'sprites/player/right_{i}.png') for i in range(1, 5)]

    # Словарь с наборами спрайтов для каждого направления движения
    animation_sprites = {
        'down': down_sprites,
        'up': up_sprites,
        'left': left_sprites,
        'right': right_sprites
    }

    # Начальное направление и набор спрайтов для анимации
    current_direction = 'down'
    current_sprites = animation_sprites[current_direction]

    player.add_component(RenderComponent(current_sprites))
    player.add_component(AnimationComponent(current_sprites, 0.285))
    player.add_component(FootstepsComponent())
    player.add_component(HitboxComponent(31, 25, 17, 40))  # Добавление хитбокса для персонажа

    return player, animation_sprites


def create_tree(x, y, scale=0.15, hitbox_width=30, hitbox_height=30, hitbox_offset_x=65, hitbox_offset_y=110):
    tree = Entity()
    original_image = pygame.image.load('sprites/tree.png')
    tree_image = pygame.transform.scale(original_image, (
        int(original_image.get_width() * scale), int(original_image.get_height() * scale)))
    tree.add_component(PositionComponent(x, y))
    tree.add_component(RenderComponent(tree_image))

    # Создание и добавление хитбокса для дерева
    tree_hitbox = HitboxComponent(hitbox_width, hitbox_height, hitbox_offset_x, hitbox_offset_y)
    tree.add_component(tree_hitbox)

    tree.add_component(TreeComponent())
    return tree


def create_menu():
    menu = Entity()
    menu_position = (100, 100)  # Установка позиции меню
    menu.add_component(
        MenuComponent(["Start", "Options", "Quit"], ["Start Game", "Options", "Quit Game"], menu_position))
    menu.add_component(PositionComponent(*menu_position))  # Добавление компонента позиции с указанием позиции меню
    menu.add_component(RenderComponent(None))  # В этом примере меню не имеет спрайта, поэтому передаем None
    return menu


def create_axe(x, y, scale=0.5, hitbox_width=20, hitbox_height=20, hitbox_offset_x=10, hitbox_offset_y=10):
    axe = Entity()
    axe.add_component(AxeComponent())
    original_image = pygame.image.load('sprites/items/axe.png')  # Загрузите текстуру топора
    axe_image = pygame.transform.scale(original_image, (
        int(original_image.get_width() * scale), int(original_image.get_height() * scale)))
    axe.add_component(PositionComponent(x, y))
    render_component = RenderComponent(axe_image)
    axe.add_component(render_component)

    # Создание и добавление хитбокса для топора
    axe_hitbox = HitboxComponent(hitbox_width, hitbox_height, hitbox_offset_x, hitbox_offset_y)
    axe.add_component(axe_hitbox)

    # Устанавливаем изображение топора в качестве его иконки
    axe.get_component(AxeComponent).icon = axe_image

    return axe


def initialize_entities():
    player, animation_sprites = create_player()
    trees = [create_tree(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(15)]

    # Создание топора
    axe = create_axe(random.randint(0, WIDTH), random.randint(0, HEIGHT))

    # Сортировка деревьев по координатам y и верхним границам хитбоксов
    trees.sort(key=lambda tree: (tree.get_component(PositionComponent).y +
                                 tree.get_component(HitboxComponent).offset_y))

    # Создаем QuadTree и добавляем деревья
    quadtree = QuadTree(pygame.Rect(0, 0, WIDTH, HEIGHT), 4)
    for tree in trees:
        pos = tree.get_component(PositionComponent)
        quadtree.insert((pos.x, pos.y))

    menu = create_menu()

    # Добавляем топор в список допустимых сущностей
    valid_entities = [player] + trees + [axe, menu]

    return player, trees, axe, quadtree, animation_sprites, menu, valid_entities
