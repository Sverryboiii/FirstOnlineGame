from src.client.events import events
from src.client.entities import player
from src.client import tick, frame, network, config
import pygame, sys

def init_player():

    selected = "UN"
    username = ""
    password = ""

    error_message = ""

    un_surf = events.LOGIN_FONT.render(username, True, config.text_color)
    error_surf = events.LOGIN_FONT.render(error_message, True, config.error_text_color)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    selected = "UN" if selected == "PW" else "PW"
                elif event.key == pygame.K_BACKSPACE:
                    if selected == "UN":
                        username = username[:-1]
                    elif selected == "PW":
                        password = password[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(username) <= 5:
                        error_message = "Username must be at least 6 characters!"
                    elif len(password) < 8:
                        error_message = "Password must be at least 8 characters!"
                elif event.unicode.isprintable():
                    if selected == "UN":
                        username += event.unicode
                    elif selected == "PW":
                        password += event.unicode


        # Draw
        events.window.blit(
            error_message, (0, 200)
        )
        events.window.blit()

    payload = {
        "op": 1
    }
    payload = network.send(payload)
    events.UID = payload["UID"]

def main():
    network.try_connect()
    init_player()

    events.player = player.Player(10, 10)
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                network.send({"op": 4, "UID": events.UID})
                pygame.quit()
                sys.exit()

        tick.tick()
        frame.frame()

if __name__ == "__main__":
    main()