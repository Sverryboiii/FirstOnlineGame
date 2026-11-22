import pygame, sys
pygame.init()

UID = 0

window = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("My First Online Game!")

# Fonts
LOGIN_FONT = pygame.font.SysFont("arial", 50)
TEXT_FONT = pygame.font.SysFont("arial", 25)

clock = pygame.time.Clock()

objects = []
player = None

draw_info = []

def quit_game():
    pygame.quit()
    sys.exit()