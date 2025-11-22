from dataclasses import dataclass
from data.static.definitions import Element, InheritedBuff

@dataclass
class CardObject:
    name: str
    damage: int
    health: int
    element: Element

@dataclass
class LeaderObject(CardObject):
    buff: InheritedBuff
    inherited_from: str