import pygame
from pygame.locals import *
from settings import WIDTH, HEIGHT, FPS
from player import Player
from world import World
import sys
from utils import play_background_music


def main():
    pygame.init()
    pygame.display.set_caption("Pixel Craft")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    world = World()
    player = Player((100, 100))
    play_background_music()

    panel_x = world.inventory_panel.x
    panel_y = world.inventory_panel.y
    panel_width = world.inventory_panel.width
    panel_height = world.inventory_panel.height

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # В основном цикле программы
            if event.type == MOUSEBUTTONDOWN:
                # Обработка нажатия на ячейку инвентаря
                mouse_x, mouse_y = event.pos
                if panel_x <= mouse_x <= panel_x + panel_width and panel_y <= mouse_y <= panel_y + panel_height:
                    rel_x = mouse_x - panel_x
                    rel_y = mouse_y - panel_y
                    col = rel_x // (world.inventory_panel.slot_width + world.inventory_panel.slot_padding)
                    row = rel_y // (world.inventory_panel.slot_height + world.inventory_panel.slot_padding)
                    index = int(row * (panel_width / world.inventory_panel.slot_width) + col)
                    world.inventory_panel.set_active_slot_index(index)  # Устанавливаем выбранную ячейку

            if event.type == KEYDOWN:
                if event.key == K_e:  # Если нажата клавиша E
                    if player.rect.colliderect(world.axe_rect):  # Если игрок находится рядом с топором
                        if world.add_item_to_player_inventory(world.axe):  # Проверяем, есть ли место в инвентаре
                            world.spawn_axe()  # Заспавнить новый топор, если предмет успешно поднят

        # Получаем состояние клавиш и обновляем состояние игрока
        keys = pygame.key.get_pressed()
        player.update(keys, clock.get_time() / 1000, world.trees)

        # Обновляем координаты камеры в соответствии с положением персонажа
        world.camera_x = player.rect.x - WIDTH // 2
        world.camera_y = player.rect.y - HEIGHT // 2

        # Отрисовываем мир с учетом камеры
        screen.fill((0, 0, 0))  # Затемняем весь экран цветом
        world.draw(screen, player, world.camera_x, world.camera_y)

        # Обновляем инвентарь в мире
        world.inventory_panel.update_inventory(world.player_inventory)

        # Обновляем экран
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
