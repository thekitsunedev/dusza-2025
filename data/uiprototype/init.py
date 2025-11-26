import pygame
from data.uiprototype import *
from data.uiprototype.navigator import *
from data.uiprototype.editor import Editor

def init():
    pygame.init()
    ctx = Context()
    scenes = {
        "MainMenu": MenuScene("scene1"),
        "Collection": CollectionScene("scene2"),
        "WorldEditor": Editor("editor")
    }
    nav = Navigator(ctx, scenes)
    nav.start("MainMenu")



