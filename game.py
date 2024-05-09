import pygame
from settings import WIDTH, HEIGHT, FPS
from player import Player
from world import World


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.world = World()
        self.player = Player(self.world.start_position)
        self.dt = 0

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000  # Преобразование из мс в секунды
            self.events()
            self.update(self.dt)
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt):
        self.player.update(dt)
        self.world.update(dt)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        self.world.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()

    def wait_for_key(self):
        pygame.event.wait()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return
