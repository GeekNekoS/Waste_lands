class GameState:
    def __init__(self):
        self.state = 'menu'

    def menu(self):
        # Логика меню
        pass

    def game(self):
        # Логика игры
        pass

    def pause(self):
        # Логика паузы
        pass

    def run(self):
        if self.state == 'menu':
            self.menu()
        elif self.state == 'game':
            self.game()
        elif self.state == 'pause':
            self.pause()
