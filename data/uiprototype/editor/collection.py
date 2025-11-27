import pygame
import pygame_menu

class CollectionCreator:
    def __init__(self, world):
        self.world = world
        self.menu = pygame_menu.Menu("", width=1920//3*2, height=1080,
                                    position=(1920//3, 0, 0), theme=pygame_menu.themes.THEME_DARK)
    
    def draw(self, ctx):
        self.menu.draw(ctx.screen)
    
    def eventHandler(self, event):
        self.menu.update(event)