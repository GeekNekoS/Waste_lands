import pygame
from pygame.locals import *
from settings import WIDTH, HEIGHT, FPS
from mvc.model.player import Player, PlayerSounds
from mvc.model.world import World
import sys
from mvc.controller.utils import play_background_music


def main():
    pygame.init()
    pygame.display.set_caption("Forgotten Spaces")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    world = World()

    # Инициализация звуков игрока
    player_sounds = PlayerSounds()

    # Создание экземпляра игрока с передачей звуков
    player = Player((100, 100), player_sounds)

    panel_x = world.inventory_panel.x
    panel_y = world.inventory_panel.y
    panel_width = world.inventory_panel.width
    panel_height = world.inventory_panel.height

    play_background_music()

    while True:
        dt = clock.tick(FPS) / 1000.0  # Время, прошедшее с прошлого кадра в секундах

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Обработка событий мыши
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if panel_x <= mouse_x <= panel_x + panel_width and panel_y <= mouse_y <= panel_y + panel_height:
                    rel_x = mouse_x - panel_x
                    rel_y = mouse_y - panel_y
                    col = rel_x // (world.inventory_panel.slot_width + world.inventory_panel.slot_padding)
                    row = rel_y // (world.inventory_panel.slot_height + world.inventory_panel.slot_padding)
                    index = int(row * (panel_width / world.inventory_panel.slot_width) + col)
                    world.inventory_panel.set_active_slot_index(index)

            # Обработка событий клавиатуры
            if event.type == KEYDOWN:
                if event.key == K_e:
                    if player.rect.colliderect(world.axe_rect):
                        if world.add_item_to_player_inventory(world.axe):
                            world.spawn_axe()

        # Получение состояния клавиш и обновление состояния игрока
        keys = pygame.key.get_pressed()
        player.update(keys, dt, world.trees)

        # Обновление координат камеры в соответствии с положением персонажа
        world.camera_x = player.rect.x - WIDTH // 2
        world.camera_y = player.rect.y - HEIGHT // 2

        # Обновление состояния мира, включая врагов
        world.update(player.rect, dt)

        # Отрисовка мира с учетом камеры
        screen.fill((0, 0, 0))  # Затемняем весь экран цветом
        world.draw(screen, player, world.camera_x, world.camera_y)

        # Отрисовка инвентаря поверх остальных элементов
        world.inventory_panel.update_inventory(world.player_inventory)
        world.inventory_panel.draw(screen)

        # Обновление экрана
        pygame.display.flip()


if __name__ == "__main__":
    main()
