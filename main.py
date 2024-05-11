import pygame
from settings import WIDTH, HEIGHT, FPS
from menu import Menu
from player import Player
from world import World
import sys


def main():
    pygame.init()
    pygame.display.set_caption("Pixel Craft")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    world = World()
    player = Player((100, 100))

    while True:
        menu = Menu(screen, player, world)  # Передаем параметры player, world
        menu.run()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
