import pygame
import sys


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.bg_color = (0, 0, 0)
        self.font = pygame.font.Font(None, 36)
        self.items = ['Start Game', 'Exit']
        self.selected_index = 0

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.items)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.items)
                    elif event.key == pygame.K_RETURN:
                        return self.selected_index  # Возвращает индекс выбранного пункта

            self.screen.fill(self.bg_color)
            self.draw_menu()
            pygame.display.flip()

    def draw_menu(self):
        for index, item in enumerate(self.items):
            if index == self.selected_index:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)
            label = self.font.render(item, True, color)
            label_rect = label.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + index * 50))
            self.screen.blit(label, label_rect)
