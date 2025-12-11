import re
from data.prototypes.search import findByName


class FightCalls:
    def __init__(self):
        super().__init__()
    

    def prepareFight(self, dungeon_name: str) -> dict | str:
        if not hasattr(self, "controller"):
            return "Controller not initialized"

        dungeon = findByName(self.controller.world.dungeons, dungeon_name)
        self.controller.fight_system.prepare(
            self.controller.deck, dungeon)

        result: dict = {}
        result["deck"] = {}
        for card in self.controller.fight_system.deck:
            result["deck"][card.name] = {
                "health": card.health,
                "damage": card.damage,
                "element": self.MAPPING["ELEMENT"][card.element.name]
            }
        
        result["enemy_deck"] = {}
        for card in self.controller.fight_system.enemy_deck:
            result["enemy_deck"][card.name] = {
                "health": card.health,
                "damage": card.damage,
                "element": self.MAPPING["ELEMENT"][card.element.name]
            }
        
        result["active_card"] = {}
        result["active_enemy"] = {}

        return result
    
    def iterateFight(self) -> dict | str:
        if not hasattr(self, "controller"):
            return "Controller not initialized"

        iter_result = [""]
        while not iter_result[0].startswith("jatekos"):
            result: dict = {}

            iter_result = self.controller.fight_system.iterate().split(";")

            if iter_result[0].startswith("jatekos"):
                result["result"] = {
                    "status": iter_result[0]
                }
                if len(iter_result) == 2:
                    reward_card = findByName(self.controller.world.collection, iter_result[1])
                    result["result"]["reward"] = {
                        "name": reward_card.name,
                        "health": reward_card.health,
                        "damage": reward_card.damage,
                        "element": self.MAPPING["ELEMENT"][reward_card.element.name]
                    }
                elif len(iter_result) == 3:
                    result["result"]["reward"] = {
                        "stat": iter_result[1],
                        "card": iter_result[2]
                    }
            else:
                result["round"] = iter_result[0]
                result["player"] = iter_result[1]
                result["action"] = iter_result[2]
                result["deck"] = {}
                for card in self.controller.fight_system.deck:
                    result["deck"][card.name] = {
                        "health": card.health,
                        "damage": card.damage,
                        "element": self.MAPPING["ELEMENT"][card.element.name]
                    }
        
                result["enemy_deck"] = {}
                for card in self.controller.fight_system.enemy_deck:
                    result["enemy_deck"][card.name] = {
                        "health": card.health,
                        "damage": card.damage,
                        "element": self.MAPPING["ELEMENT"][card.element.name]
                    }
            
                active_card = self.controller.fight_system.current_card
                if active_card is None:
                    result["active_card"] = {}
                else:
                    result["active_card"] = {
                        "name": active_card.name,
                        "health": active_card.health,
                        "damage": active_card.damage,
                        "element": self.MAPPING["ELEMENT"][active_card.element.name]
                    }

                active_enemy = self.controller.fight_system.current_enemy
                if active_enemy is None:
                    result["active_enemy"] = {}
                else:
                    result["active_enemy"] = {
                        "name": active_enemy.name,
                        "health": active_enemy.health,
                        "damage": active_enemy.damage,
                        "element": self.MAPPING["ELEMENT"][active_enemy.element.name]
                    }
            yield result