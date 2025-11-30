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
<<<<<<< HEAD
        "CardSelection": CardSelection("cardselection")
=======
        "SaveSelect": SaveSelect("saveselect")
>>>>>>> 14fcb1714c45323852ada9829da69d1287268660
    }
    nav = Navigator(ctx, scenes)
    nav.start("Starter")



