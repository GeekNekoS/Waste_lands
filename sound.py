import pygame
from components import Component


class SoundComponent(Component):
    def __init__(self, sound_file):
        self.sound = pygame.mixer.Sound(sound_file)

    def play(self):
        self.sound.play()
