import pygame
pygame.init()
from data.uiprototype import *
from data.uiprototype.navigator import *
from data.uiprototype.editor import Editor
from data.prototypes.connector import Connector


def init():
    
    ctx = Context()
    scenes = {
        "Starter":  StarterMenu("scene1"),
        "MainMenu": MenuScene("scene2"),
        "Collection": CollectionScene("scene3"),
        "WorldEditor": Editor("editor"),
        "WorldSelect": WorldSelect("worldselect"),
        "AllCards" : AllCards("allcards")
    }
    nav = Navigator(ctx, scenes)
    nav.start("Starter")



