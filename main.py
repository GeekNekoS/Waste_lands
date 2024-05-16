import sys
import pygame
from utils import draw_debug_line
from systems import MovementSystem, RenderSystem, CollisionSystem
from game_state import GameState
from settings import debug, WIDTH, HEIGHT, FPS
from entities import initialize_entities
from components import (
    MenuComponent,
    InventoryComponent,
    VelocityComponent,
    AnimationComponent,
    PositionComponent,
    FootstepsComponent,
    RenderComponent,
    HitboxComponent,
    AxeComponent
)

import random
from entities import create_axe


def handle_pickup(player, valid_entities, picked_items):
    player_hitbox = player.get_component(HitboxComponent)
    player_position = player.get_component(PositionComponent)

    if not player_hitbox or not player_position:
        return

    for entity in valid_entities[:]:  # Проходим по копии списка, чтобы избежать проблем с удалением во время итерации
        if entity in picked_items:
            continue

        entity_hitbox = entity.get_component(HitboxComponent)
        entity_position = entity.get_component(PositionComponent)

        if not entity_hitbox or not entity_position:
            continue

        if player_hitbox.get_rect(player_position).colliderect(entity_hitbox.get_rect(entity_position)):
            player_inventory = player.get_component(InventoryComponent)
            if player_inventory.add_item(entity):
                picked_items.append(entity)
                valid_entities.remove(entity)
                print(f"Picked up item: {entity}")
                break


pygame.init()

# Инициализация
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Создание игровых сущностей
player, trees, axe, quadtree, animation_sprites, menu, valid_entities = initialize_entities()

# Инициализация систем
movement_system = MovementSystem()
render_system = RenderSystem()
collision_system = CollisionSystem(quadtree)

# Инициализация игрового состояния
game_state = GameState()

# Инициализация флагов для отслеживания нажатия и отпускания клавиш
key_pressed = {pygame.K_a: False, pygame.K_d: False, pygame.K_w: False, pygame.K_s: False}

current_direction = 'down'
valid_entities = [player] + trees + [axe, menu]
picked_items = []  # Список подобранных предметов
menu_visible = False

print('Начальное количество подобранных предметов:', len(picked_items))
print("Вызов функции handle_pickup перед циклом while")
running = True
while running:
    dt = clock.tick(FPS) / 1000  # время между кадрами в секундах

    # Обновление флагов для нажатия и отпускания клавиш
    for key in key_pressed:
        key_pressed[key] = pygame.key.get_pressed()[key]

    menu_entities = [entity for entity in valid_entities if entity.get_component(MenuComponent)]

    # Обработка событий клавиатуры для меню
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Проверяем нажатие клавиши "E" для подбора предмета
            if event.key == pygame.K_e:
                print("Список сущностей перед вызовом функции handle_pickup:", valid_entities)
                # Обновление состояния игры
                handle_pickup(player, valid_entities, picked_items)
                print('Количество подобранных предметов после подбора топора:', len(picked_items))

            # Если меню видимо
            if menu_visible:
                for entity in menu_entities:
                    menu_component = entity.get_component(MenuComponent)
                    if menu_component:
                        # Переключение между пунктами меню при нажатии клавиш вверх и вниз
                        if event.key == pygame.K_UP:
                            menu_component.move_selection(-1)
                        elif event.key == pygame.K_DOWN:
                            menu_component.move_selection(1)
                        # Выбор пункта меню при нажатии клавиши ENTER
                        elif event.key == pygame.K_RETURN:
                            selected_option = menu_component.options[menu_component.selected_option]
                            if selected_option == "Start Game":
                                game_state.state = 'game'
                            elif selected_option == "Options":
                                # Логика для перехода к экрану опций
                                pass
                            elif selected_option == "Quit Game":
                                pygame.quit()
                                sys.exit()
            else:
                # Если меню не видимо, переключение видимости при нажатии клавиши ESC
                if event.key == pygame.K_ESCAPE:
                    menu_visible = not menu_visible
                if event.key == pygame.K_LEFT:
                    # Перемещение активной ячейки влево
                    player.get_component(InventoryComponent).move_active_slot(-1)
                elif event.key == pygame.K_RIGHT:
                    # Перемещение активной ячейки вправо
                    player.get_component(InventoryComponent).move_active_slot(1)

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

    # Установка направления движения, чтобы определить анимацию персонажа
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

    # Отрисовка персонажа
    screen.blit(
        player.get_component(AnimationComponent).frames[player.get_component(AnimationComponent).current_frame],
        (player.get_component(PositionComponent).x, player.get_component(PositionComponent).y))

    # Отрисовка линии от персонажа до топора при включенном режиме отладки (debug)
    draw_debug_line(screen, player, axe)

    # Отрисовка персонажа и деревьев
    for tree in trees:
        tree_render = tree.get_component(RenderComponent)
        tree_position = tree.get_component(PositionComponent)
        if tree_render.image:
            tree_hitbox = tree.get_component(HitboxComponent)
            tree_top = tree_position.y + tree_hitbox.offset_y  # Верхняя граница хитбокса дерева
            player_position = player.get_component(PositionComponent)
            player_hitbox = player.get_component(HitboxComponent)
            player_bottom = player_position.y + player_hitbox.offset_y + player_hitbox.height  # Нижняя граница хитбокса персонажа
            if player_bottom >= tree_top:
                screen.blit(player.get_component(AnimationComponent).frames[
                                player.get_component(AnimationComponent).current_frame],
                            (player_position.x, player_position.y))
                screen.blit(tree_render.image, (tree_position.x, tree_position.y))
            else:
                screen.blit(tree_render.image, (tree_position.x, tree_position.y))

    # Отрисовка топора
    axe_position = axe.get_component(PositionComponent)
    axe_hitbox = axe.get_component(HitboxComponent)
    axe_render = axe.get_component(RenderComponent)
    if axe_render.image:
        screen.blit(axe_render.image, (axe_position.x, axe_position.y))

    # Отладочная отрисовка хитбокса
    if debug:
        # Рисуем хитбоксы для деревьев
        for tree in trees:
            tree_position = tree.get_component(PositionComponent)
            tree_hitbox = tree.get_component(HitboxComponent)
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(tree_position.x + tree_hitbox.offset_x,
                                                              tree_position.y + tree_hitbox.offset_y,
                                                              tree_hitbox.width, tree_hitbox.height), 2)

        # Получаем компоненты позиции и хитбокса персонажа
        player_position = player.get_component(PositionComponent)
        player_hitbox = player.get_component(HitboxComponent)

        # Рисуем хитбокс персонажа
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(player_position.x + player_hitbox.offset_x,
                                                          player_position.y + player_hitbox.offset_y,
                                                          player_hitbox.width, player_hitbox.height), 2)

    # Отрисовка инвентаря
    player.get_component(InventoryComponent).draw_inventory(screen, WIDTH, HEIGHT)

    # Отрисовка меню
    render_system.draw_menu(screen, menu.get_component(MenuComponent))

    pygame.display.flip()

pygame.quit()
sys.exit()
