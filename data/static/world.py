from dataclasses import dataclass
from data.static.cards import *
from data.static.dungeon import Dungeon

@dataclass
class World:
    name: str
    cards: list[CardObject]
    leaders: list[LeaderObject]
    dungeons: list[Dungeon]
    collection: list[CardObject]
    difficulty: int = 0