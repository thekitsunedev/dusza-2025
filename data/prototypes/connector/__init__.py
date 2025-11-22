from pathlib import Path
from data.prototypes.controller import Controller
from data.prototypes.connector.cards import CardCalls
from data.prototypes.connector.dungeon import DungeonCalls
from data.prototypes.connector.fight import FightCalls
from data.prototypes.connector.world import WorldCalls

class Connector(CardCalls, DungeonCalls, FightCalls, WorldCalls):
    def __init__(self):
        self.DATA_PATH = Path(__file__).resolve()
        while self.DATA_PATH.parts[-1] != "data":
            self.DATA_PATH = self.DATA_PATH.parent
        super().__init__()
        self.controller: Controller

        self.MAPPING = {
            "ELEMENT": {
                "FIRE": "Tűz",
                "WATER": "Víz",
                "EARTH": "Föld",
                "AIR": "Levegő"
            },
            "REWARD": {
                "HEALTH": "Életerő",
                "DAMAGE": "Sebzés",
                "CARD": "Kártya"
            },
            "DUNTYPE": {
                "SIMPLE": "Egyszerű",
                "SMALL": "Kis",
                "BIG": "Nagy"
            },
            "BUFF": {
                "HEALTH": "Életerő",
                "DAMAGE": "Sebzés"
            }
        }