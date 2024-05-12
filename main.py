import pygame
from settings import WIDTH, HEIGHT, FPS
from menu import Menu
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

    # Создаем экземпляр меню
    menu = Menu(screen, player, world)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Получаем состояние клавиш и обновляем состояние игрока
        keys = pygame.key.get_pressed()
        player.update(keys, clock.get_time() / 1000, world.trees)

        # Обновляем координаты камеры в соответствии с положением персонажа
        world.camera_x = player.rect.x - WIDTH // 2
        world.camera_y = player.rect.y - HEIGHT // 2

        # Отрисовываем мир с учетом камеры
        screen.fill((0, 0, 0))  # Затемняем весь экран цветом
        world.draw(screen, player, world.camera_x, world.camera_y)

        # Обновляем экран
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
