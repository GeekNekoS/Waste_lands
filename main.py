import pygame
from settings import WIDTH, HEIGHT, FPS
from world import World


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    world = World(WIDTH, HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dt = clock.tick(FPS) / 1000  # Получаем dt и преобразуем из мс в секунды

        world.update(dt)  # Обновляем мир
        screen.fill((135, 206, 250))  # Цвет фона (светло-голубой, например, небо)
        world.draw(screen)  # Рисуем мир

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
