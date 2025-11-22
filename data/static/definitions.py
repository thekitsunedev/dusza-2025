from enum import Enum, auto

class Element(Enum):
    """
    Stores the element, and its opposite to which it deals the half damage.
    """

    FIRE = "AIR"
    WATER = "EARTH"
    AIR = "FIRE"
    EARTH = "WATER"


class InheritedBuff(Enum):
    """
    Marks the type of buff a leader card inherits from a generic card.
    """

    HEALTH = auto()
    DAMAGE = auto()


class DungeonReward(Enum):
    """
    Marks the type of reward given to the card defeating the last opponent.
    """

    HEALTH = ";eletero"
    DAMAGE = ";sebzes"
    CARD = ""


class DungeonType(Enum):
    """
    Marks the type of the dungeon.
    """

    SIMPLE = "egyszeru"
    SMALL = "kis"
    BIG = "nagy"