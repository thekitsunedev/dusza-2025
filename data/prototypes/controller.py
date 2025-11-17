from data.static.simple_card import CardObject
from data.static.leader_card import LeaderObject
from data.static.dungeon import DungeonObject
import data.static.global_definitions as GLOB
from math import ceil

game_cards: list[CardObject] = []       # list of all the basic game cards
leader_cards: list[LeaderObject] = []   # list of leader cards
dungeons: list[DungeonObject] = []      # list of dungeons
collection: list[CardObject] = []       # list of cards that the player owns
deck: list[CardObject] = []             # list of cards that you take to a dungeon


def createCard(name: str,
                strength: int,
                health: int,
                element: GLOB.Elements) -> None:
    """
    Creates a card and appends it to the game_cards list
    arguments:
        name: name of the card [len() <= 16]
        strength: base dmg of the card [0 < DMG <= 100]
        health: health of the card [0 < HP <= 100]
        element: the element of the card, [Elements.(FIRE|WATER|AIR|EARTH)]
    """

    # Prevent duplicates
    for card in game_cards:
        if name[:16] == card.name:
            return
    card = CardObject(name, health, strength, element)
    game_cards.append(card)

def createLeader(name: str,
                 inherit_from: str,
                 inherit_buff: GLOB.InheritBuff) -> None:
    """
    Creates a leader and appends it to the leader_cards list
    arguments:
        name: name of the card [len() <= 16]
        inherit_from: the name of the card to inherit from
        inherit_buff: which stat should be buffed [InheritBuff.(HEALTH|STRENGTH)]
    """
    # prevent duplicates
    for leader in leader_cards:
        if name[:16] == leader.name:
            return
        
    for card in game_cards:
        if card.name == inherit_from:
            inherit_from = card
            break
    
    leader = LeaderObject(name, inherit_from, inherit_buff)
    leader_cards.append(leader)

def createDungeon(name: str,
                    dun_type: GLOB.DungeonTypes,
                    reward: GLOB.DungeonRewards,
                    card_names: list[str],
                    leader_name: str = "") -> None:
    """
    Creates a dungeon and appends it to the dungeons list
    arguments:
        name: name of the dungeon [len() <= 20]
    """
    # prevent duplicates
    for dungeon in dungeons:
        if name[:20] == dungeon.name:
            return
    
    cards = []
    for cname in card_names:
        lookup = [cname == c.name for c in game_cards]
        if any(lookup):
            cards.append(game_cards[lookup.index(True)])
    
    leader = LeaderObject
    for leader in leader_cards:
        if leader_name == leader.name:
            leader = leader
            break
    
    dungeon = DungeonObject(name, dun_type, reward, cards, leader)
    dungeons.append(dungeon)

def addToCollection(name: str) -> None:
    """
    Adds a card from the game_cards to the player's collection.
    arguments:
        name: name of the card to add
    """
    # Check for already owned cards
    for card in collection:
        if card.name == name:
            return
    
    for card in game_cards:
        if card.name == name:
            collection.append(card.clone())

def createDeck(cards: list[str]) -> None:
    """
    Creates a new deck from the cards the player owns from their collection.
    arguments:
        cards: list of the name of them cards to put in a deck.
    """
    deck.clear()
    for cname in cards:
        lookup = [cname == card.name for card in collection]
        if not any(lookup):
            continue
        if len(deck) >= ceil(len(collection) / 2):
            break
        deck.append(collection[lookup.index(True)])

def cardReward() -> str:
    """
    Rewards a card to the player from the game cards.
    returns the name of the rewarded card
    """
    for card in game_cards:
        if not any([card.name == owned.name for owned in collection]):
            collection.append(card)
            return card.name


def canVisitBigDungeon():
    return len(collection) < len(game_cards)