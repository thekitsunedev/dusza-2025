from dataclasses import dataclass
from data.static.definitions import ElementAdvantage, InheritedBuff

@dataclass
class CardObject:
    name: str
    health: int
    damage: int
    element: ElementAdvantage

@dataclass
class LeaderObject(CardObject):
    buff: InheritedBuff