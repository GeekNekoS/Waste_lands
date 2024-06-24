import pygame


player_sprites = "assets/sprites/player/"
items_sprites = "assets/sprites/items/"

pygame.mixer.init()
footstep_sounds = [
    pygame.mixer.Sound('assets/sounds/footsteps/footstep_1.wav'),
    pygame.mixer.Sound('assets/sounds/footsteps/footstep_2.wav'),
    pygame.mixer.Sound('assets/sounds/footsteps/footstep_3.wav')
]
