from data.static.definitions import ElementAdvantage, InheritedBuff
from data.static.card import CardObject

class LeaderObject(CardObject):
    def __init__(
            self,
            name: str,
            inherit_from: CardObject,
            inherited_buff: InheritedBuff
        ):
        """
        LeaderObject:
            Class of a leader card, inherits from a simple card (CardObject).
        
        CardObject():
            name: str[1 - 16 $azAZ] Name of the card.
            inherit_from: <CardObject> The card to inherit.
            inherited_buff: <InheritedBuff> Buffed stat of the card.
        
        Any values that exceed the given range
        will be capped to match their limit.
        """
        if isinstance(inherited_buff, InheritedBuff):
            self._buff = inherited_buff
        else:
            raise TypeError(f"Invalid type {type(inherited_buff)} for 'inherited_buff'")

        damage_multiplier = 2 if inherited_buff is InheritedBuff.DAMAGE else 1
        health_multiplier = 2 if inherited_buff is InheritedBuff.HEALTH else 1

        super().__init__(
            inherit_from.name,
            inherit_from.damage * damage_buff,
            inherit_from.health * damage_health,
            inherit_from.element
        )
