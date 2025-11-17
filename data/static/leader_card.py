from data.static.global_definitions import Elements, InheritBuff
from data.static.simple_card import CardObject

class LeaderObject:
    def __init__(self, name: str,
                 inherit_from: CardObject,
                 inherit_buff: InheritBuff):
        self._name: str = name[:16]
        self.health = inherit_from.health * inherit_buff.value[0]
        self.strength = inherit_from.strength * inherit_buff.value[1]
        self._element = inherit_from.element

        self.__inherited_from: CardObject = inherit_from
        self.__inherit_buff: InheritBuff = inherit_buff

    @property
    def name(self) -> str:
        """
        Name of the card
        """
        return self._name
    
    @property
    def element(self) -> Elements:
        """
        Element of the card
        """
        return self._element

    @property
    def health(self) -> int:
        """
        Health of the card
        """
        return self._health
    
    @health.setter
    def health(self, val: int) -> None:
        """
        Set the health of card
        """
        if val <= 0:
            self._health = 0
        elif val > 100:
            self._health = 100
        else:
            self._health = val

    @property
    def strength(self) -> int:
        """
        strength of the card
        """
        return self._strength
    
    @strength.setter
    def strength(self, val: int) -> None:
        """
        Set the strength of card
        """
        if val <= 0:
            self._strength = 0
        elif val > 100:
            self._strength = 100
        else:
            self._strength = val

    def __repr__(self):
        return f"<LeaderObject name={self._name}, element={self._element.name}, health={self._health}, strength={self._strength}>"
    
    def clone(self):
        return LeaderObject(self._name, self.__inherited_from, self.__inherit_buff)