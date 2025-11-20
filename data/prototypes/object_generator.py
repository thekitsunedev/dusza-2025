from data.static.definitions import *
from data.static.cards import *
from data.static.dungeon import Dungeon


def createCard(name: str, health: int,
               damage: int, element: Element) -> CardObject:
    name = name[:16]
    health = min(max(health, 0), 100)
    damage = min(max(damage, 2), 100)
    return CardObject(name, health, damage, element)


def createLeader(name: str, inherit_from: CardObject,
                 buff: InheritedBuff) -> LeaderObject:
    name = name[:16]
    health = inherit_from.health * (2 if buff == InheritedBuff.HEALTH else 1)
    damage = inherit_from.damage * (2 if buff == InheritedBuff.DAMAGE else 1)
    element = inherit_from.element
    return LeaderObject(name, health, damage, element, buff)


def createDungeon(name: str,
        dungeon_type: DungeonType,
        dungeon_reward: DungeonReward,
        cards: list[CardObject],
        leader: LeaderObject | None) -> Dungeon:
    name = name[:20]
    match(dungeon_type):
        case DungeonType.SIMPLE:
            cards = cards[:1]
            leader = None
        case DungeonType.SMALL:
            cards = cards[:3]
            leader = leader
            if leader == None:
                raise ValueError("Leader not specified")
        case DungeonType.BIG:
            cards = cards[:5]
            leader = leader
            if leader == None:
                raise ValueError("Leader not specified")

    return Dungeon(name, dungeon_type, dungeon_reward, cards, leader)