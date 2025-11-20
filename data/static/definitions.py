from enum import Enum

class Element(Enum):
    """
    Stores the element, and its opposite to which it deals the double damage.
    """

    FIRE = "AIR"
    WATER = "EARTH"
    AIR = "FIRE"
    EARTH = "WATER"


### Replace <None> with string of locale name if locales get implemented.
class InheritedBuff(Enum):
    """
    Marks the type of buff a leader card inherits from a generic card.
    """

    HEALTH = "leader.buff.health"
    DAMAGE = "leader.buff.damage"


class DungeonReward(Enum):
    """
    Marks the type of reward given to the card defeating the last opponent.
    """

    HEALTH = "dungeon.reward.health"
    DAMAGE = "dungeon.reward.damage"
    CARD = "dungeon.reward.card"


class DungeonType(Enum):
    """
    Marks the type of the dungeon.
    """

    SIMPLE = "dungeon.type.simple"
    SMALL = "dungeon.type.small"
    BIG = "dungeon.type.big"