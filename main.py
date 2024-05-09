import pygame
from settings import WIDTH, HEIGHT, FPS
from player import Player
from world import World
from menu import Menu
import sys


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    player = Player((100, 100))
    world = World()

    game_started = False  # Добавляем флаг для отслеживания начала игры

    while True:  # Заменяем однократный запуск на цикл для возможности возврата в меню
        items = ['Continue' if game_started else 'Start Game', 'Exit']
        menu = Menu(screen, items=items)
        selected_action = menu.run()

        if selected_action == 1:  # Если пользователь выбрал 'Exit'
            break

        game_started = True  # Обновляем флаг, когда игра начата

        running = True
        while running:
            dt = clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Обработка нажатия Esc
                        running = False  # Выйти из игрового цикла, вернуться в меню

            keys = pygame.key.get_pressed()
            player.update(keys, dt, world.trees)
            screen.fill((135, 206, 235))
            world.draw(screen, player)
            pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
