from src.client.events import events
from src.client import config
import pygame

def frame():
    events.window.fill(config.background_color)

    for name, data in events.draw_info.items():
        if name == "players":
            for pos in data:
                pygame.draw.circle(
                    events.window,
                    config.player_color,
                    pos,
                    config.player_radius
                )

    pygame.display.flip()