import pygame

class Context:
    def __init__(self):
        self.screen = pygame.display.set_mode((1200,1200))
        self.font = pygame.font.SysFont("Arial", 80)
        self.font2 = pygame.font.SysFont("Arial", 20)