from data.static.global_definitions import DungeonTypes, DungeonRewards
from data.static.simple_card import CardObject
from data.static.leader_card import LeaderObject

class DungeonObject:
    def __init__(self, name: str,
                 dun_type: DungeonTypes,
                 reward: DungeonRewards,
                 cards: list[CardObject],
                 leader: LeaderObject):
        
        self._name = name[:20]
        self._type = dun_type
        if self._type.name == "BIG":
            self._reward = DungeonRewards.CARD
        else:
            self._reward = reward
        
        self._cards = []
        for card in cards[:self._type.value[0]]:
            self._cards.append(card.clone())
        if self._type.value[1] == 1:
            self._cards.append(leader.clone())
    

    @property
    def name(self) -> str:
        return self._name

    @property
    def cards(self) -> list:
        return self._cards
    
    @property
    def dunType(self) -> str:
        return self._type.name
    
    @property
    def reward(self) -> DungeonRewards:
        return self._reward
    
    def __repr__(self) -> str:
        return f"<DungeonObject name={self._name}, type={self._type.name}, cards={self._cards}, reward={self._reward.name if self._reward != None else None}>"
    
    def clone(self):
        return DungeonObject(self._name, self._type, self._reward, self._cards[:-1], self._cards[-1])