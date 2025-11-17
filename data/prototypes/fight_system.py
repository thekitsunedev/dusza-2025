from math import floor
from os.path import join
import data.static.global_definitions as GLOB
import data.prototypes.controller as controller
from data.static.dungeon import DungeonObject
from data.static.simple_card import CardObject
from data.static.leader_card import LeaderObject

WORK_DIR: str = ""

class Arena:
    def __init__(self):        
        self._deck = []
        self._dungeon_enemies = []

        self.round_index: int = 1 # The current round
        self.iter_phase: bool = True # iteration phase of curr. round (used to determine who's turn it is.)
        self.curr_player_card: CardObject | None = None
        self.curr_enemy_card:  CardObject | LeaderObject | None = None


    def prepare(self, dun_name: str, outfile: str) -> None:
        """
        Prepare arena for a match
        """
        self.__dun_name = dun_name
        self.outfile = join(WORK_DIR, outfile)

        # Reset the arena
        self._deck = []
        self._dungeon_enemies = []
        self.round_index = 1
        self.iter_phase = True

        # Prepare cards
        for card in controller.deck:
            self._deck.append(card.clone())
        
        # Dungeon
        self.dungeon: DungeonObject
        for dungeon in controller.dungeons:
            if dungeon.name == self.__dun_name:
                self.dungeon = dungeon
                break
        for dun_card in self.dungeon.cards:
            self._dungeon_enemies.append(dun_card.clone())

        
    def iterate(self) -> str:
        return_str: str = ""

        if len(self._deck) == 0 and self.curr_player_card == None:
            # Player lost
            return "jatekos vesztett"
        elif len(self._dungeon_enemies) == 0 and self.curr_enemy_card == None:
            # Reward player
            curr_card_name = self.curr_player_card.name

            if self.dungeon.reward == GLOB.DungeonRewards.CARD:
                reward = controller.cardReward()
                return f"jatekos nyert;{reward}"
            else:
                winner_card: CardObject
                # Get card from collection
                for card in controller.collection:
                    if card.name == curr_card_name:
                        winner_card = card
                        break
                
                winner_card.health += self.dungeon.reward.value[0]
                winner_card.strength += self.dungeon.reward.value[1]
                reward_str = getattr(GLOB.Locale, self.dungeon.reward.name).value
                return f"jatekos nyert;{reward_str};{winner_card.name}"
            
            

        if self.iter_phase:
            ## Dungeon's turn
            return_str += "kazamata"
            if self.curr_enemy_card == None:
                # Play card if none is playing
                self.curr_enemy_card = self._dungeon_enemies[0]
                return_str += f";kijatszik;{self.getCardAttr(self.curr_enemy_card)}"
            else:
                # Attack player
                attack_result = self.attack()
                
                return_str += f";tamad{attack_result}"
                if self.curr_player_card.health == 0:
                    self.curr_player_card = None
                    self._deck.pop(0)
        else:
            ## Player's turn
            return_str += "jatekos"
            # Play card if none is playing:
            if self.curr_player_card == None:
                self.curr_player_card = self._deck[0]
                return_str +=  f";kijatszik;{self.getCardAttr(self.curr_player_card)}"
            else:
                # Attack enemy
                attack_result = self.attack(False)
                
                return_str += f";tamad{attack_result}"
                if self.curr_enemy_card.health == 0:
                    self.curr_enemy_card = None
                    self._dungeon_enemies.pop(0)
                

        return_str = f"{self.round_index}.kor;{return_str}"

        # Step over to next round after everyone's step.
        if not self.iter_phase:
            self.round_index += 1

            # Separate round logs
            return_str += "\n"
        # Go to next iter.
        self.iter_phase ^= True

        return return_str
    

    def attack(self, initiator = True) -> None:
        """
        if initiator: enemy attacks player
        else: player attacks enemy
        """
        dmg_multiplier: float = 1.0 
        if initiator:
            if self.curr_enemy_card.element.name == self.curr_enemy_card.element.value:
                dmg_multiplier = 0.5
            elif self.curr_enemy_card.element.name != self.curr_player_card.element.name:
                dmg_multiplier = 2.0
        
            attack_dmg = int(floor(self.curr_enemy_card.strength * dmg_multiplier))
            self.curr_player_card.health -= attack_dmg
            return f";{self.curr_enemy_card.name};{attack_dmg};{self.curr_player_card.name};{self.curr_player_card.health}"
        else:
            if self.curr_player_card.element.name == self.curr_enemy_card.element.value:
                dmg_multiplier = 0.5
            elif self.curr_player_card.element.name != self.curr_enemy_card.element.name:
                dmg_multiplier = 2.0
        
            attack_dmg = int(floor(self.curr_player_card.strength * dmg_multiplier))
            self.curr_enemy_card.health -= attack_dmg
            return f";{self.curr_player_card.name};{attack_dmg};{self.curr_enemy_card.name};{self.curr_enemy_card.health}"


    def getCardAttr(self, card: CardObject | LeaderObject) -> str:
        name =  card.name
        strength = card.strength
        health = card.health
        element = getattr(GLOB.Locale, card.element.name).value
        return f"{name};{strength};{health};{element}"
    

    @property
    def deck(self):
        return self._deck
    
    @property
    def dungeonDeck(self):
        return self._dungeon_enemies


arena = Arena()
def init(dungeon_name: str, outfile: str):
    """
    Initializes the matching system.
    arguments:
        dungeon_name: name of the dungeon to attack.
        outfile: name of the file for match results, empty for no outfile
    """
    arena.prepare(dungeon_name, outfile)


def start() -> None:
    """
    Start the match (w/ autoiter)
    """
    with open(arena.outfile, "a") as file:
        file.write(f"harc kezdodik;{arena.dungeon.name}\n\n")
        res: str = ""
        while not res.startswith("jatekos"):
            res = arena.iterate()
            file.write(res+"\n")