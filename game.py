import pygame
from settings import WIDTH, HEIGHT, FPS
from player import Player
from world import World


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.world = World()
        self.player = Player((100, 100))
        self.dt = 0

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()
            self.draw()
            pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt):
        self.player.update(dt)
        self.world.update(dt)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Очистка экрана
        self.player.draw(self.screen)  # Отрисовка игрока

    def wait_for_key(self):
        pygame.event.wait()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return
