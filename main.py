import pygame
from settings import WIDTH, HEIGHT, FPS
from player import Player
from world import World


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    player = Player((100, 100))
    world = World()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Обновление времени для фреймрейта
        for event in pygame.event.get():  # Получение и обработка списка событий
            if event.type == pygame.QUIT:  # Проверка события "Закрыть окно"
                running = False

        keys = pygame.key.get_pressed()  # Получение состояния клавиш
        player.update(keys, dt, world.trees)  # Обновление состояния игрока
        screen.fill((135, 206, 235))  # Очистка экрана с заливкой цветом

        world.draw(screen, player)  # Отрисовка мира и игрока
        pygame.display.flip()  # Обновление содержимого всего экрана

    pygame.quit()  # Закрытие и очистка ресурсов Pygame


if __name__ == "__main__":
    main()
