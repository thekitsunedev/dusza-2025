import json
import os
from pathlib import Path
from data.prototypes.object_generator import createCard
from data.prototypes.parser.world import loadWorld
from data.static.definitions import *
from data.static.world import World

DATA_PATH: Path = Path(__file__).resolve()
while DATA_PATH.parts[-1] != "data":
    DATA_PATH = DATA_PATH.parent

def save(world: World, save_name: str = "default_world") -> None:
    """
    Save world data to saves/<world_name>.json
    world_name defaults to default_world
    """
    SAVE_PATH: Path = DATA_PATH.joinpath(f"saves/{save_name}.json")
    save_data: dict = {}

    # Export world name
    save_data["world_name"] = world.name

    # Export collection
    save_data["collection"] = {}
    for card in world.collection:
        card_data: dict = {}
        card_data["health"] = card.health
        card_data["damage"] = card.damage
        card_data["element"] = card.element.name
        save_data["collection"][card.name] = card_data
    
    # Export difficulty
    save_data["difficulty"] = world.difficulty

    # Save output
    with open(SAVE_PATH, "w") as file:
        json.dump(save_data, file)



def load(save_name: str) -> World:
    # Validate file path
    save_path: str = ""
    for file in Path(DATA_PATH).joinpath("saves").glob("*"):
        file_name = file.parts[-1]
        if not file_name.endswith(".json"):
            continue
        if file_name.split(".")[0] == save_name:
            save_path = f"saves/{file_name}"
    
    if save_path == "":
        raise FileNotFoundError("Save '{save_name}' not found")


    with open(DATA_PATH.joinpath(save_path)) as file:
        save_data: dict = json.load(file)
        # Load in world and delete default collection
        world = loadWorld(save_data["world_name"])
        world.collection.clear()

        # Load saved collection
        for card_name in save_data["collection"]:
            card_data = save_data["collection"][card_name]
            card_health = card_data["health"]
            card_damage = card_data["damage"]
            card_element = getattr(Element, card_data["element"])
            card = createCard(card_name, card_damage,
                              card_health, card_element)
            world.collection.append(card)

        # Load difficulty
        world.difficulty = save_data["difficulty"]

    return world

def delete(save_name: str) -> None:
    SAVE_PATH = DATA_PATH.joinpath(f"saves/{save_name}.json")
    try:
        os.remove(SAVE_PATH)
    except:
        ...