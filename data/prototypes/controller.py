from dataclasses import replace
from math import ceil
from data.prototypes.fight_system import FightSystem
import data.prototypes.save_parser as save
from data.prototypes.search import findCardByName
from data.prototypes.world_parser import loadWorld
from data.static.cards import CardObject
from data.static.world import World


class Controller:
    def __init__(self, name: str = "default_world", load: bool = False):
        """
        name: str > default_world
            name of the world to load | create
        load: bool > False
            ?False: create a new world
            ?True: load a save
        """
        if load:
            self.world = save.load(name)
        else:
            self.world = loadWorld(name)
    
        self.deck: list[CardObject] = []

        self.fight_system = FightSystem(self.world)
    
    def createDeck(self, cards: list[str]) -> list[CardObject]:
        """
        Creates a new deck, and returns the cards in the deck.
        
        cards: list[str]
            List with the name of the cards, if deck limit is reached,
            the extra cards will be skipped.
        """

        DECK_MAX_LEN = ceil(len(self.world.collection) / 2)
        self.deck.clear()
        for card_name in cards:
            if len(self.deck) >= DECK_MAX_LEN:
                continue
            card = findCardByName(self.world.collection, card_name)
            if card == None:
                continue
            self.deck.append(card)

        return self.deck
    

    # Returns true if big dungeons can be visited
    # (player can be rewarded with cards)
    @property
    def canVisitBigDungeon(self):
        return len(self.world.collection) < len(self.world.cards)