import pygame
from data.uiprototype import *
from data.uiprototype.navigator import *

def init():
    pygame.init()
    scenes = {
        "MainMenu": MenuScene("scene1"),
        "Collection": CollectionScene("scene2")
    }
    ctx = Context()
    nav = Navigator(ctx, scenes)
    nav.start("MainMenu")



