from os.path import join
from data.static.simple_card import CardObject
from data.static.leader_card import LeaderObject
from data.static.dungeon import DungeonObject
from data.static.global_definitions import DungeonTypes, Locale, DungeonRewards
import data.prototypes.controller as controller

WORK_DIR: str = ""

def exportWorld(filename: str) -> None:
    """
    Exports each card, leader and dungeon into a file.
    arguments:
        filename: str | name of the file to write to
    """
    path = join(WORK_DIR, filename)
    with open(path, "a") as file:
        # card export
        for card in controller.game_cards:
            file.write(f"kartya;{card.name};{card.strength};{card.health};{getattr(Locale, card.element.name).value}\n")
        file.write("\n")

        # leader export
        for leader in controller.leader_cards:
            file.write(f"vezer;{leader.name};{leader.strength};{leader.health};{getattr(Locale, leader.element.name).value}\n")
        file.write("\n")

        # dungeon export
        for dungeon in controller.dungeons:
            # Format cards
            leader = ""
            dun_cards = ""
            for card in dungeon.cards:
                if type(card) is LeaderObject:
                    leader = ";"+card.name
                else:
                    dun_cards += f",{card.name}"
            # Get reward
            reward = ""
            if dungeon.reward != DungeonRewards.CARD:
                reward = ";" + getattr(Locale, dungeon.reward.name).value

            dungeon_type = ""
            match(dungeon.dunType):
                case "SIMPLE":
                    dungeon_type = "egyszeru"
                case "SMALL":
                    dungeon_type = "kis"
                case "BIG":
                    dungeon_type = "nagy"
            file.write(f"kazamata;{dungeon_type};{dungeon.name};{''.join(dun_cards[1:])}{leader}{reward}\n")
        file.close()


def exportPlayer(filename: str) -> None:
    """
    Exports the player collection and the card names of the last used deck to a file.
    arguments:
        filename: str | name of the file to write to
    """
    path = join(WORK_DIR, filename)
    with open(path, "a") as file:
        # Collection
        for card in controller.collection:
            file.write(f"gyujtemeny;{card.name};{card.strength};{card.health};{getattr(Locale, card.element.name).value}\n")
        file.write("\n")

        # Last used deck
        for card in controller.deck:
            file.write(f"pakli;{card.name}\n")
        file.close()