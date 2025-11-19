from dataclasses import dataclass
from data.static.global_definitions import DungeonType, DungeonReward
from data.static.cards import *

@dataclass
class Dungeon:
    name: str
    dungeon_type: DungeonType
    reward: DungeonReward
    cards: list[CardObject]
    leader: LeaderObject | None = None