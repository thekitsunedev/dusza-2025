from enum import Enum

class Elements(Enum):
    """Key values represent their resistance for an other element."""
    FIRE = "AIR"
    WATER = "EARTH"
    EARTH = "WATER"
    AIR = "FIRE"

class DungeonTypes(Enum):
    """
    TYPE = (simple_card_count, leader_card_count)
    """
    SIMPLE = (1, 0)
    SMALL = (3, 1)
    BIG = (5, 1)

class DungeonRewards(Enum):
    """
    TYPE = (health_bonus, strength_bonus) || None [Card reward]
    """
    STRENGTH = (0, 1)
    HEALTH = (2, 0)
    CARD = None

class InheritBuff(Enum):
    """
    TYPE = (health_multiplier, strength_multiplier)
    """
    HEALTH = (2, 1)
    STRENGTH = (1, 2)

 
class Locale(Enum):
    """
    Locale mask, use getattr()
    """
    EARTH = "fold"
    AIR = "levego"
    WATER = "viz"
    FIRE = "tuz"
    HEALTH = "eletero"
    STRENGTH = "sebzes"
    CARD = ""