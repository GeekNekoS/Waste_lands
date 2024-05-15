import pygame


player_sprites = "sprites/player/"
items_sprites = "sprites/items/"

pygame.mixer.init()
footstep_sounds = [
    pygame.mixer.Sound('../sounds/footsteps/footstep_1.wav'),
    pygame.mixer.Sound('../sounds/footsteps/footstep_2.wav'),
    pygame.mixer.Sound('../sounds/footsteps/footstep_3.wav')
]
