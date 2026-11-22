from src.client.events import events
from src.client import config
import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def frame(self):
        pygame.draw.circle(
            events.window,
            config.player_color,
            (self.x, self.y),
            50
        )