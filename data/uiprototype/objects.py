import pygame

class Context:
    def __init__(self):
        self.screen = pygame.display.set_mode((1920,1080))
        self.font = pygame.font.SysFont("Arial", 80)
        self.font2 = pygame.font.SysFont("Arial", 20)
        self.kartyafont = pygame.font.SysFont("arial", 22)