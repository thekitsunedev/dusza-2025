from data.static.cards import CardObject, LeaderObject
from data.static.definitions import Element
from data.static.dungeon import Dungeon



def findByName(cards: list[CardObject | LeaderObject | Dungeon], name: str) -> CardObject | LeaderObject | Dungeon:
    """
    Finds card by name, and returns it's object
    card_types:
    - CardObject
    - LeaderObject
    - Dungeon
    """
    card = CardObject("", 0, 0, Element.FIRE)
    for card in cards:
        if card.name == name:
            card = card
            break
    return card
    

def findNotOwned(cards: list[CardObject], collection: list[CardObject]) -> CardObject:
    found: CardObject
    for card in cards:
        if any([card.name == owned.name for owned in collection]):
            continue
        found = card
        break
    return found