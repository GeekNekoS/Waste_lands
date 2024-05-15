import pygame
import random
from animation import AnimationComponent
from systems import MovementSystem, RenderSystem, CollisionSystem
from quadtree import QuadTree
from game_state import GameState
from settings import debug, WIDTH, HEIGHT, FPS
from components import (
    HitboxComponent,
    PositionComponent,
    VelocityComponent,
    RenderComponent,
    InventoryComponent,
    SoundComponent,
    FootstepsComponent
)

pygame.init()

# Инициализация
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Entity:
    def __init__(self):
        self.components = {}

    def add_component(self, component):
        self.components[type(component)] = component

    def get_component(self, component_type):
        return self.components.get(component_type, None)


# Создание игровых сущностей
player = Entity()
player.add_component(PositionComponent(100, 100))
player.add_component(VelocityComponent(0, 0))

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

# Добавление компонентов
player.add_component(RenderComponent(current_sprites))
player.add_component(AnimationComponent(current_sprites, 0.285))
player.add_component(InventoryComponent(4))
player.add_component(FootstepsComponent())
player.add_component(HitboxComponent(17, 40, 31, 25))  # Добавление хитбокса для персонажа

# Создание деревьев и других объектов
quadtree = QuadTree(pygame.Rect(0, 0, WIDTH, HEIGHT), 4)
trees = []  # список деревьев с компонентами позиции и изображения

# Инициализация систем
movement_system = MovementSystem()
render_system = RenderSystem()
collision_system = CollisionSystem(quadtree)

# Инициализация игрового состояния
game_state = GameState()

# Инициализация флагов для отслеживания нажатия и отпускания клавиш
key_pressed = {pygame.K_a: False, pygame.K_d: False, pygame.K_w: False, pygame.K_s: False}

running = True
while running:
    dt = clock.tick(FPS) / 1000  # время между кадрами в секундах

    # Обновление флагов для нажатия и отпускания клавиш
    for key in key_pressed:
        key_pressed[key] = pygame.key.get_pressed()[key]

    # Обработка событий клавиатуры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Установка скорости в зависимости от нажатых клавиш
    vx = (key_pressed[pygame.K_d] - key_pressed[pygame.K_a]) * 1
    vy = (key_pressed[pygame.K_s] - key_pressed[pygame.K_w]) * 1

    # Установка скорости персонажа
    player_velocity = player.get_component(VelocityComponent)

    # Если движение идет и по горизонтали, и по вертикали, устанавливаем обе компоненты скорости в ноль
    if vx != 0 and vy != 0:
        player_velocity.vx = 0
        player_velocity.vy = 0
    else:
        # Установка скорости по осям X и Y
        player_velocity.vx = vx
        player_velocity.vy = vy

    # Установка направления движения
    if vx != 0:
        current_direction = 'right' if vx > 0 else 'left'
    elif vy != 0:
        current_direction = 'down' if vy > 0 else 'up'

    if vx != 0 or vy != 0:
        animation_component = player.get_component(AnimationComponent)
        animation_component.update(dt)
        footsteps_component = player.get_component(FootstepsComponent)
        footsteps_component.play_footstep(animation_component)

    # Обновление систем
    movement_system.update([player])
    collision_system.update([player])

    # Изменение анимации в зависимости от направления движения
    player.get_component(RenderComponent).image = animation_sprites[current_direction]
    player.get_component(AnimationComponent).frames = animation_sprites[current_direction]

    # Отрисовка
    screen.fill((0, 0, 0))

    # Отрисовка персонажа и деревьев
    screen.blit(player.get_component(AnimationComponent).frames[player.get_component(AnimationComponent).current_frame],
                (player.get_component(PositionComponent).x, player.get_component(PositionComponent).y))

    # Отладочная отрисовка хитбокса
    if debug:
        # Получаем компоненты позиции и хитбокса персонажа
        player_position = player.get_component(PositionComponent)
        player_hitbox = player.get_component(HitboxComponent)

        # Получаем прямоугольник хитбокса с учетом смещения и позиции персонажа
        hitbox_rect = player_hitbox.get_rect(player_position)

        # Отображаем хитбокс
        pygame.draw.rect(screen, (255, 0, 0), hitbox_rect, 2)

    # Отрисовка деревьев
    for tree in trees:
        screen.blit(tree.get_component(RenderComponent).image, (tree.get_component(PositionComponent).x,
                                                                tree.get_component(PositionComponent).y))

    valid_entities = [player]
    for tree in trees:
        valid_entities.append(tree)

    render_system.update(valid_entities, screen)

    pygame.display.flip()

pygame.quit()
