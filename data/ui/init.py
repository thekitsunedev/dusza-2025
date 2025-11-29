import pygame
pygame.init()
from data.ui import *
from data.ui.navigator import *
from data.ui.editor import Editor
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



