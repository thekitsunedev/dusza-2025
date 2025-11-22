from data.static.cards import CardObject, LeaderObject
from data.static.dungeon import Dungeon



def findByName(cards: list[CardObject | LeaderObject | Dungeon], name: str) -> CardObject | LeaderObject | Dungeon | None:
    """
    Finds card by name, and returns it's object
    card_types:
    - CardObject
    - LeaderObject
    - Dungeon
    """
    for card in cards:
        if card.name == name:
            return card
    return None

def findNotOwned(cards: list[CardObject], collection: list[CardObject]) -> CardObject | None:
    found: CardObject | None = None
    for card in cards:
        if any([card.name == owned.name for owned in collection]):
            continue
        found = card
        break
    return found