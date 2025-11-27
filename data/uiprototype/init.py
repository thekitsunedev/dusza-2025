import pygame
pygame.init()
from data.uiprototype import *
from data.uiprototype.navigator import *
from data.uiprototype.editor import Editor

def init():
    
    ctx = Context()
    scenes = {
        "Starter":  StarterMenu("scene1"),
        "MainMenu": MenuScene("scene2"),
        "Collection": CollectionScene("scene3"),
        "WorldEditor": Editor("editor")
    }
    nav = Navigator(ctx, scenes)
    nav.start("Starter")



