from dataclasses import replace
from math import floor
from random import random
from data.prototypes.search import findCardByName, findNotOwned
from data.static.cards import CardObject, LeaderObject
from data.static.definitions import DungeonReward
from data.static.dungeon import Dungeon
from data.static.world import World


class FightSystem:
    def __init__(self, world: World):
        self.world = world
        self.deck: list[CardObject] = []
        self.enemy_deck: list[CardObject | LeaderObject] = []
        self.current_card: CardObject | None
        self.current_enemy: CardObject | LeaderObject | None
        self.ELEMENTMAP: dict = {
            "FIRE": "tuz",
            "WATER": "viz",
            "EARTH": "fold",
            "AIR": "levego"
        }
    
    def iterate(self) -> str:
        result = ""

        # Player lost
        if all([card.health == 0 for card in self.deck]):
            self.round_phase = -1 # Disable iteration until reset
            return "jatekos vesztett"

        # Player won
        elif all([card.health == 0 for card in self.enemy_deck]):
            self.round_phase = -1 # Disable iteration until reset
            result = "jatekos nyert"
            match(self.dungeon.reward):
                # Health reward (+2HP)
                case DungeonReward.HEALTH:
                    card_name = self.deck[self.card_index].name
                    card = findCardByName(self.world.collection, card_name)
                    if card is None:
                        raise Exception("Card not found")
                    card.health = min(card.health + 2, 100)
                    result += f";eletero;{card_name}"

                # Damage reward (+1DMG)
                case DungeonReward.DAMAGE:
                    card_name = self.deck[self.card_index].name
                    card = findCardByName(self.world.collection, card_name)
                    if card is None:
                        raise Exception("Card not found")
                    card.damage = min(card.damage + 1, 100)
                    result += f";sebzes;{card_name}"

                # Card reward
                case DungeonReward.CARD:
                    card = findNotOwned(self.world.cards, self.world.collection)
                    if card is None:
                        raise Exception("Cannot reward player with card")
                    self.world.collection.append(replace(card))
                    result += f";{card.name}"
            return result

        # Enemy's turn
        elif self.round_phase == 0:
            if self.current_enemy is None:
                self.current_enemy = self.enemy_deck[self.enemy_index]
                card_name = self.current_enemy.name
                card_damage = self.current_enemy.damage
                card_health = self.current_enemy.health
                card_element = self.ELEMENTMAP.get(self.current_enemy.element.name)
                result += f";kazamata;kijatszik;{card_name};{card_damage};{card_health};{card_element}"
            else:
                if self.current_card is None:
                    raise Exception("Current card is None")
                elemental_multiplier = self.getElementalMultiplier(self.current_enemy, self.current_card)
                damage = floor(self.current_enemy.damage * elemental_multiplier)
                if self.world.difficulty > 0:
                    damage = round(damage * (1 + random() * self.world.difficulty / 10))
                self.current_card.health = max(self.current_card.health - damage, 0)
                result += f";kazamata;tamad;{self.current_enemy.name};{damage};{self.current_card.name};{self.current_card.health}"
                if self.current_card.health == 0:
                    self.current_card = None
                    self.card_index += 1

        # Player's turn
        elif self.round_phase == 1:
            if self.current_card is None:
                self.current_card = self.deck[self.card_index]
                card_name = self.current_card.name
                card_damage = self.current_card.damage
                card_health = self.current_card.health
                card_element = self.ELEMENTMAP.get(self.current_card.element.name)
                result += f";jatekos;kijatszik;{card_name};{card_damage};{card_health};{card_element}"
            else:
                if self.current_enemy is None:
                    raise Exception("Current enemy is None")
                elemental_multiplier = self.getElementalMultiplier(self.current_card, self.current_enemy)
                damage = floor(self.current_card.damage * elemental_multiplier)
                if self.world.difficulty > 0:
                    damage = round(damage * (1 - random() * self.world.difficulty / 20))
                self.current_enemy.health = max(self.current_enemy.health - damage, 0)
                result += f";jatekos;tamad;{self.current_card.name};{damage};{self.current_enemy.name};{self.current_enemy.health}"
                if self.current_enemy.health == 0:
                    self.current_enemy = None
                    self.enemy_index += 1
        
        self.__round_phase_old = self.round_phase
        self.round_phase = (self.round_phase + 1) % 2
        result = f"{self.round}.kor{result}"
        if self.round_phase == 1 and self.__round_phase_old == 0:
            self.round += 1
        return result

    # Get elemental multiplier for damage
    def getElementalMultiplier(self, attacker: CardObject | LeaderObject,
               attacked: CardObject | LeaderObject,) -> float:
        
        elemental_multiplier: float = 1.0
        if attacker.element.name == attacked.element.value:
            elemental_multiplier = 0.5
        elif attacker.element.name != attacked.element.name:
            elemental_multiplier = 2.0
        return elemental_multiplier

    # Prepare for a new fight
    def prepare(self, deck: list[CardObject], dungeon: Dungeon) -> None:
        self.reset()

        self.deck = []
        for card in deck:
            self.deck.append(replace(card)) 
        self.dungeon = dungeon
        self.enemy_deck = []
        for card in self.dungeon.cards:
            self.enemy_deck.append(replace(card))
        
        if self.dungeon.leader != None:
            self.enemy_deck.append(replace(self.dungeon.leader))

    # Reset variables
    def reset(self) -> None:
        self.round = 1
        self.round_phase = 0
        self.__round_phase_old = 0
        self.card_index = 0
        self.enemy_index = 0
        self.deck.clear()
        self.enemy_deck.clear()
        self.current_card = None
        self.current_enemy = None