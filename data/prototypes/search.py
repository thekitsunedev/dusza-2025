from data.static.cards import CardObject, LeaderObject
from data.static.dungeon import Dungeon


def findCardByName(cards: list[CardObject], name: str) -> CardObject | None:
    for card in cards:
        if card.name == name:
            return card
    return None


def findLeaderByName(leaders: list[LeaderObject], name: str) -> LeaderObject | None:
    for leader in leaders:
        if leader.name == name:
            return leader
    return None

def findDungeonByName(dungeons: list[Dungeon], name: str) -> Dungeon | None:
    for dungeon in dungeons:
        if dungeon.name == name:
            return dungeon
    return None

def findCardFromCollection(collection: list[CardObject], name: str) -> CardObject | None:
    for card in collection:
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