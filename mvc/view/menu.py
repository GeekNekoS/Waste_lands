# Доисторическая версия menu, надо будет дописать и внедрить в игру

from mvc.controller.utils import play_background_music
from mvc.model.player import Player
from mvc.model.world import World

import pygame
import sys
import os
import json
from typing import Callable, Dict
from settings import WIDTH, HEIGHT


class Menu:
    screen: pygame.Surface
    player: Player
    world: World
    bg_color: tuple
    font: pygame.font.Font
    game_started: bool
    save_exists: bool
    selected_index: int
    items: list[str]
    menu_actions: Dict[str, Callable[[], None]]

    def __init__(self, screen: pygame.Surface, player: Player, world: World, game_started: bool = False, save_exists: bool = False) -> None:
        """Инициализация объекта меню."""
        self.screen = screen
        self.player = player
        self.world = world
        self.bg_color = (0, 0, 0)
        self.font = pygame.font.Font(None, 36)
        self.game_started = game_started
        self.save_exists = save_exists
        self.selected_index = 0
        self.menu_actions = {
            'Start Game': self.start_game,
            'Continue': self.continue_game,
            'Save Game': self.save_game,
            'Exit': self.exit_game
        }
        self.update_items()

    def update_items(self) -> None:
        """Обновление списка пунктов меню в зависимости от состояния игры."""
        if self.game_started:
            if self.save_exists:
                self.items = ['Start New Game', 'Continue', 'Save Game', 'Exit']
            else:
                self.items = ['Start New Game', 'Save Game', 'Exit']
        else:
            self.items = ['Start Game', 'Exit']

    def run(self) -> None:
        """Запуск цикла отображения и обработки событий меню."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_index = max(0, self.selected_index - 1)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = min(len(self.items) - 1, self.selected_index + 1)
                    elif event.key == pygame.K_RETURN:
                        selected_item = self.items[self.selected_index]
                        self.menu_actions[selected_item]()
                    elif event.key == pygame.K_ESCAPE:
                        if self.items == ['Start New Game', 'Continue', 'Save Game', 'Exit']:
                            self.menu_actions['Exit']()

            self.screen.fill(self.bg_color)
            self.draw_menu()
            pygame.display.flip()

    def draw_menu(self) -> None:
        """Отрисовка меню на экране."""
        for index, item in enumerate(self.items):
            color = (255, 0, 0) if index == self.selected_index else (255, 255, 255)
            label = self.font.render(item, True, color)
            label_rect = label.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + index * 50))
            self.screen.blit(label, label_rect)

    def start_game(self) -> None:
        """Начало новой игры."""
        print("Starting new game...")
        self.game_started = True
        self.save_exists = False  # Новая игра, поэтому сохранение не существует
        play_background_music()  # Запуск фоновой музыки
        self.run_game_loop()

    def continue_game(self) -> None:
        """Продолжение игры."""
        print("Continuing game...")
        self.load_game()
        self.run_game_loop()

    def run_game_loop(self) -> None:
        """Запуск игрового цикла после начала игры или продолжения."""
        game_running = True
        while game_running:
            dt = pygame.time.Clock().tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_running = False

            keys = pygame.key.get_pressed()
            self.player.update(keys, dt, self.world.trees)

            # Обновляем координаты камеры на основе положения игрока
            self.world.camera_x = max(0, min(self.player.rect.x - WIDTH // 2, self.world.camera_x))
            self.world.camera_y = max(0, min(self.player.rect.y - HEIGHT // 2, self.world.camera_y))

            # Отображаем мир с учетом камеры
            self.screen.fill((135, 206, 235))
            self.world.draw(self.screen, self.player, self.world.camera_x, self.world.camera_y)
            pygame.display.flip()

        # После завершения игры возвращаемся в меню
        self.game_started = False
        self.save_exists = os.path.exists('savegame.json')
        self.update_items()
        self.run()

    def save_game(self) -> None:
        """Сохранение текущего состояния игры в файл."""
        print("Saving game...")
        save_data = {
            'player_position': {
                'x': self.player.rect.x,
                'y': self.player.rect.y
            },
            'world': {
                'trees': self.world.get_save_data()
            }
        }
        try:
            with open('savegame.json', 'w') as f:
                json.dump(save_data, f)
            print("Game saved successfully.")
            self.save_exists = True  # Устанавливаем значение в True после успешного сохранения
            self.update_items()  # Обновляем список пунктов меню
        except Exception as e:
            print(f"Error saving game: {e}")

    def exit_game(self) -> None:
        """Выход из игры, остановка музыки и завершение работы программы."""
        if not self.game_started and not os.path.exists('savegame.json'):
            # Если игра не начата и сохранения отсутствуют
            self.save_exists = False  # Устанавливаем значение в False
            self.update_items()  # Обновляем список пунктов меню
        print("Exiting game...")
        pygame.mixer.music.stop()  # Остановка фоновой музыки
        pygame.quit()
        sys.exit()

    def load_game(self) -> None:
        """Загрузка сохраненного состояния игры из файла."""
        if not os.path.exists('savegame.json'):
            print("No save file found.")
            return
        with open('savegame.json', 'r') as f:
            save_data = json.load(f)
        self.player.rect.x = save_data['player_position']['x']
        self.player.rect.y = save_data['player_position']['y']
        self.player.update_hitbox()  # Обновляем хитбокс игрока
        if 'world' in save_data:
            self.world.load_from_save(save_data['world']['trees'], (self.player.rect.x, self.player.rect.y))  # Передаем координаты игрока
        print("Game loaded successfully.")
