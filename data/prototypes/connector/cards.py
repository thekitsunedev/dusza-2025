from math import ceil

class CardCalls:

    def __init__(self):
        super().__init__()
    
    def fetchCards(self, *filter: str) -> dict | str:
        """
        Fetches currently loaded in cards
        Filters:
        - cards
        - leaders
        - collection
        - deck
        """
        if not hasattr(self, "controller"):
            return "Controller not initialized"

        result: dict = {}
        no_filter = len(filter) == 0

        # Cards
        if no_filter or "cards" in filter:
            if len(filter) == 1:
                buffer = result
            else:
                result["cards"] = {}
                buffer = result["cards"]
            
            for card in self.controller.world.cards:
                buffer[card.name] = {
                    "health": card.health,
                    "damage": card.damage,
                    "element": self.MAPPING["ELEMENT"][card.element.name]
                }
        
        # Leaders
        if no_filter or "leaders" in filter:
            if len(filter) == 1:
                buffer = result
            else:
                result["leaders"] = {}
                buffer = result["leaders"]
            
            for card in self.controller.world.leaders:
                buffer[card.name] = {
                    "health": card.health,
                    "damage": card.damage,
                    "element": self.MAPPING["ELEMENT"][card.element.name]
                }
        
        # Collection
        if no_filter or "collection" in filter:
            if len(filter) == 1:
                buffer = result
            else:
                result["collection"] = {}
                buffer = result["collection"]
            
            for card in self.controller.world.collection:
                buffer[card.name] = {
                    "health": card.health,
                    "damage": card.damage,
                    "element": self.MAPPING["ELEMENT"][card.element.name]
                }
        
        # Deck
        if no_filter or "deck" in filter:
            if len(filter) == 1:
                buffer = result
            else:
                result["deck"] = {}
                buffer = result["deck"]
            
            for card in self.controller.deck:
                buffer[card.name] = {
                    "health": card.health,
                    "damage": card.damage,
                    "element": self.MAPPING["ELEMENT"][card.element.name]
                }
        
        return result

    def createDeck(self, cards: list[str]) -> dict | str:
        if not hasattr(self, "controller"):
            return "Controller not initialized"
        result: dict = {}
        for card in self.controller.createDeck(cards):
            result[card.name] = {
                "health": card.health,
                "damage": card.damage,
                "element": self.MAPPING["ELEMENT"][card.element.name]
            }
        
        return result
    
    @property
    def deck_limit(self) -> int:
        return ceil(len(self.controller.world.collection)/2)