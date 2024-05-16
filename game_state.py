import pygame
import sys


class GameState:
    def __init__(self):
        self.state = 'menu'

    def menu(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.items)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.items)
                elif event.key == pygame.K_RETURN:
                    selected_item = self.items[self.selected_option]
                    if selected_item == "Start":
                        self.state = 'game'
                    elif selected_item == "Options":
                        # Логика для перехода к экрану опций
                        pass
                    elif selected_item == "Quit":
                        pygame.quit()
                        sys.exit()

    def game(self):
        # Логика игры
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'pause'  # Переключение в состояние паузы

    def pause(self):
        # Логика паузы
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'game'  # Возврат к игровому состоянию

    def resume(self):
        if self.state == 'pause':
            self.state = 'game'

    def run(self):
        if self.state == 'menu':
            self.menu()
        elif self.state == 'game':
            self.game()
        elif self.state == 'pause':
            self.pause()
