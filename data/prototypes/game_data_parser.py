from pathlib import Path
import json
from data.static.global_definitions import Elements, DungeonTypes, InheritBuff, DungeonRewards
import data.prototypes.controller as controller


def parse() -> None:
    """
    Parses the static/game_data.json file for the game mode.
    """
    content_path = Path(__file__).resolve().parent.parent / "static/game_data.json"
    with open(content_path, "r") as f:
        parsed = json.load(f)
        
        # Cards
        cards = parsed["cards"]
        for card in cards:
            card_data = cards[card]
            controller.createCard(card,
                                 card_data["strength"],
                                 card_data["health"],
                                 getattr(Elements, card_data["element"]))
        
        # Leaders
        leaders = parsed["leaders"]
        for leader in leaders:
            leader_data = parsed["leaders"][leader]
            controller.createLeader(leader,
                                    leader_data["inherit"],
                                    getattr(InheritBuff, leader_data["buff"]))
        
        # Dungeons
        dungeons = parsed["dungeons"]
        for dungeon in dungeons:
            dun_data = dungeons[dungeon]
            controller.createDungeon(dungeon,
                                    getattr(DungeonTypes, dun_data["type"]),
                                    getattr(DungeonRewards, dun_data["reward"]),
                                    dun_data["cards"],
                                    dun_data["leader"])
        
        # Colleciton
        collection = parsed["collection"]
        for card_name in collection:
            controller.addToCollection(card_name)