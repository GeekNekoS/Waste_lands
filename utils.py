import pygame


def play_background_music():
    pygame.mixer.init()
    pygame.mixer.music.load('dark-background-sounds.mp3')
    pygame.mixer.music.play(-1)
