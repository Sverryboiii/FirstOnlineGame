from src.client.events import events
from src.client import config, network
import pygame

def tick():
    events.clock.tick(config.FPS)

    events.draw_info = network.send({"op": 3}) # Request draw info

    keys = pygame.key.get_pressed()
    held_chars = [
        char for char in "wasd"
        if keys[pygame.key.key_code(char)]
    ]
    network.send({"op": 2, "KEYS": held_chars, "UID": events.UID})