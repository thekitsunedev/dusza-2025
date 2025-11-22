from data.prototypes.controller import Controller
from data.static.definitions import DungeonType


class DungeonCalls:
    def __init__(self):
        super().__init__()
    
    def fetchDungeons(self) -> dict | str:
        if not hasattr(self, "controller"):
            return "Controller not initialized"
        result: dict = {}
        
        for dungeon in self.controller.world.dungeons:
            available = True
            if dungeon.type is DungeonType.BIG:
                if not self.controller.canVisitBigDungeon:
                    available = False
            
            cards = {}
            for card in dungeon.cards:
                cards[card.name] = {
                    "health": card.health,
                    "damage": card.damage,
                    "element": self.MAPPING["ELEMENT"][card.element.name]
                }

            leader = {}
            if dungeon.leader is not None:
                leader[dungeon.leader.name] = {
                    "health": dungeon.leader.health,
                    "damage": dungeon.leader.damage,
                    "buff": self.MAPPING["BUFF"][dungeon.leader.buff.name],
                    "element": self.MAPPING["ELEMENT"][dungeon.leader.element.name]
                }

            result[dungeon.name] = {
                "available": available,
                "reward": self.MAPPING["REWARD"][dungeon.reward.name],
                "type": self.MAPPING["DUNTYPE"][dungeon.dungeon_type.name],
                "cards": cards,
                "leader": leader
            }

        return result