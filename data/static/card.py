from data.static.definitions import ElementAdvantage

class CardObject:
    def __init__(
            self,
            name: str,
            damage: int,
            health: int,
            element: ElementAdvantage
        ):
        """
        CardObject:
            Class of a simple card.

        CardObject():
            name: <str[1 - 16 $azAZ]> Name of the card.
            damage: <int[2 - 100]> Default damage the card deals.
            health: <int[1 - 100]> Default health of the card.
            element: <ElementAdvantage> Element of the card.
        
        Any values that exceed the given range
        will be capped to match their limit.
        """

        if not isinstance(name, str):
            raise TypeError(f"Invalid type {type(name)} for 'name'")
        elif not name.isascii():
            raise ValueError(f"Name must only contain ASCII charcters")
        else:
            self._name = name[:16]

        if isinstance(health, int):
            self._health = min(max(health, 2), 100)
        else:
            raise TypeError(f"Invalid type {type(health)} for 'health'")
    
        if isinstance(damage, int):
            self._damage = min(max(damage, 1), 100)
        else:
            raise TypeError(f"Invalid type {type(health)} for 'health'")

        if isinstance(element, ElementAdvantage):
            self._element = element
        else:
            raise TypeError(f"Invalid type {type(element)} for 'element'")
    

    # Card name
    @property
    def name(self) -> str:
        return self._name
    
    # Card health
    @property
    def health(self) -> int:
        return self._health
    
    @property.setter
    def health(self, new_health: int) -> None:
        self._health = min(max(new_health, 0), 100)
    
    # Card damage
    @property
    def damage(self) -> int:
        return self._damage
    
    @property.setter
    def damage(self, new_damage: int) -> None:
        self._damage = min(max(new_damage, 2), 100)
    
    # Card Element
    @property
    def element(self) -> ElementAdvantage:
        return self._element
    
    @property
    def weakness(self) -> ElementAdvantage:
        return getattr(ElementAdvantage, self._element.value)

    
    # Debug
    def __repr__(self):
        return f"<CardObject name={self._name} health={self._health} damage={self._damage} element={self._element} weakness={self.weakness}>"