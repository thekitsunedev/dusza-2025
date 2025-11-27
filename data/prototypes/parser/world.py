from dataclasses import replace
import json
from pathlib import Path
from data.prototypes.object_generator import *
from data.prototypes.search import findByName
from data.static.definitions import *
from data.static.cards import *
from data.static.dungeon import Dungeon
from data.static.world import World

DATA_PATH: Path = Path(__file__).resolve()
while DATA_PATH.parts[-1] != "data":
    DATA_PATH = DATA_PATH.parent

def loadWorld(world_name: str = "") -> World:
    # look for the world data given name or fall back to default
    world_path: str = ""
    for file in Path(DATA_PATH).joinpath("custom_worlds").glob("*"):
        file_name = file.parts[-1]
        # Skip non JSON files
        if not file_name.endswith(".json"):
            continue
        
        if file_name.split(".")[0] == world_name:
            world_path = f"custom_worlds/{file_name}"
            break

    world_path = world_path or "static/default_world.json"

    # Parsing
    cards: list[CardObject] = []
    leaders: list[LeaderObject] = []
    dungeons: list[Dungeon] = []
    collection: list[CardObject] = []
    difficulty: int

    with open(DATA_PATH.joinpath(world_path)) as file:
        parsed_data: dict = json.load(file)

        # Parse difficulty
        difficulty = parsed_data["difficulty"]

        # Parse cards
        for card_name in parsed_data["cards"]:
            card_data = parsed_data["cards"][card_name]
            card_health = card_data["health"]
            card_damage = card_data["damage"]
            card_element = getattr(Element, card_data['element'])
            card = createCard(card_name, card_damage,
                              card_health, card_element)
            cards.append(card)
        
        # Parse leaders
        for leader_name in parsed_data["leaders"]:
            leader_data = parsed_data["leaders"][leader_name]
            leader_inherit = leader_data["inherit"]
            leader_buff = getattr(InheritedBuff, leader_data["buff"])
            inherit_card = findByName(cards, leader_inherit)
            if inherit_card == None:
                raise Exception(f"Card not found {leader_inherit}")
            leader = createLeader(leader_name, inherit_card, leader_buff)
            leaders.append(leader)

        # Parse dungeons
        for dungeon_name in parsed_data["dungeons"]:
            dungeon_data = parsed_data["dungeons"][dungeon_name]
            dungeon_type = getattr(DungeonType, dungeon_data["type"])
            dungeon_reward = getattr(DungeonReward, dungeon_data["reward"])
            dungeon_cards = []
            for card_name in dungeon_data["cards"]:
                card = findByName(cards, card_name)
                if card == None:
                    raise Exception(f"Card not found {card_name}")
                dungeon_cards.append(card)
            dungeon_leader = findByName(leaders, dungeon_data["leader"])
            dungeon = createDungeon(dungeon_name, dungeon_type,
                                    dungeon_reward, dungeon_cards,
                                    dungeon_leader)
            dungeons.append(dungeon)

        # Parse collection
        for card_name in parsed_data["collection"]:
            card = findByName(cards, card_name)
            if card == None:
                raise Exception(f"Card not found {card_name}")
            collection.append(replace(card))

    world_name = world_name or "default_world"

    return World(world_name, cards, leaders, dungeons, collection, difficulty)
