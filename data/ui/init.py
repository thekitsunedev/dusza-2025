import pygame
pygame.init()
from data.ui import *
from data.ui.navigator import *
from data.ui.editor import Editor
from data.ui.save import SaveSelect
from data.prototypes.connector import Connector


def init():
    
    ctx = Context()
    scenes = {
        "Starter":  StarterMenu("scene1"),
        "MainMenu": MenuScene("scene2"),
        "Collection": CollectionScene("scene3"),
        "WorldEditor": Editor("editor"),
        "WorldSelect": WorldSelect("worldselect"),
        "AllCards" : AllCards("allcards"),
        "Dungeons" : Dungeons("dungeons"),
        "DungeonSelection": DungeonSelection("dungeonselection"),
        "Fight" : Fight("fight"),
        "CardSelection": CardSelection("cardselection"),
        "SaveSelect": SaveSelect("saveselect")
    }
    nav = Navigator(ctx, scenes)
    nav.start("Starter")



