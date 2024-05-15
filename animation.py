import pygame
from components import Component


class AnimationComponent(Component):
    def __init__(self, frames, frame_rate):
        self.frames = frames
        self.frame_rate = frame_rate
        self.current_frame = 0
        self.time_since_last_frame = 0

    def update(self, dt):
        self.time_since_last_frame += dt
        if self.time_since_last_frame >= self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.time_since_last_frame = 0

    def get_current_frame(self):
        return self.frames[self.current_frame]
