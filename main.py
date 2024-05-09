import pygame
from settings import WIDTH, HEIGHT, FPS
from world import World
from player import Player
from menu import Menu
import sys


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    menu = Menu(screen)
    selection = menu.run()
    if selection == 1:  # Если выбран "Exit"
        pygame.quit()
        sys.exit()

    world = World(WIDTH, HEIGHT)
    player = Player((100, 100))

    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Преобразование времени в секунды
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update(keys, dt)
        screen.fill((135, 206, 235))  # Светло-голубой фон
        world.draw(screen)
        player.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
