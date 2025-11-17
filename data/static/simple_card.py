from data.static.global_definitions import Elements

class CardObject:
    def __init__(self, name: str,
                 health: int,
                 strength: int,
                 element: Elements):
        self._name: str = name[:16]
        self.health = health
        self.strength = strength
        self.element = element

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
    
    @element.setter
    def element(self, element: Elements) -> None:
        """
        Sets element of card
        """
        self._element = element

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
        return f"<CardObject name={self._name}, element={self._element.name}, health={self._health}, strength={self._strength}>"
    
    def clone(self):
        return CardObject(self._name, self._health, self._strength, self._element)