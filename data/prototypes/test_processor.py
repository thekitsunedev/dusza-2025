from dataclasses import replace
from pathlib import Path
from data.prototypes import controller
from data.prototypes.controller import Controller
from data.prototypes.object_generator import createCard, createDungeon, createLeader
from data.prototypes.search import findByName
from data.static.definitions import DungeonReward, DungeonType, Element, InheritedBuff
from data.static.world import World


def start(path: str) -> None:
    WORKDIR = Path(path)
    ELEMENT_MASK: dict = {
        "tuz": Element.FIRE,
        "viz": Element.WATER,
        "levego": Element.AIR,
        "fold": Element.EARTH
    }

    controller: Controller = Controller("", test_mode=True)

    with open(WORKDIR.joinpath("in.txt"), "r") as file:
        for line in file:
            if line == "":
                continue
            command = line.strip().split(";")
            try:
                match(command[0]):
                    case "uj kartya":
                        name = command[1]
                        damage = int(command[2])
                        health = int(command[3])
                        element = ELEMENT_MASK[command[4]]
                        card = createCard(name, damage, health, element)
                        controller.world.cards.append(card)
                    case "uj vezer":
                        name = command[1]
                        inherit = findByName(controller.world.cards, command[2])
                        match(command[3]):
                            case "sebzes":
                                buff = InheritedBuff.DAMAGE
                            case "eletero":
                                buff = InheritedBuff.HEALTH
                        leader = createLeader(name, inherit, buff)
                        controller.world.leaders.append(leader)
                    case "uj kazamata":
                        """
                        $1          | $2    | $3    | $4    | $5
                        ;egyszeru   ;name   ;cards  ;reward
                        ;kis        ;name   ;cards  ;leader ;reward
                        ;nagy       ;name   ;cards  ;leader
                        """
                        match(command[1]):
                            case "egyszeru":
                                dun_type = DungeonType.SIMPLE
                                match(command[4]):
                                    case "eletero":
                                        reward = DungeonReward.HEALTH
                                    case "sebzes":
                                        reward = DungeonReward.DAMAGE
                            case "kis":
                                dun_type = DungeonType.SMALL
                                match(command[5]):
                                    case "eletero":
                                        reward = DungeonReward.HEALTH
                                    case "sebzes":
                                        reward = DungeonReward.DAMAGE
                            case "nagy":
                                dun_type = DungeonType.BIG
                                reward = DungeonReward.CARD
                        name = command[2]
                        cards = []
                        for card_name in command[3].split(","):
                            cards.append(findByName(controller.world.cards, card_name))
                        if dun_type is not DungeonType.SIMPLE:
                            leader = findByName(controller.world.leaders, command[4])
                        else:
                            leader = None
                        dungeon = createDungeon(name, dun_type, reward, cards, leader)
                        controller.world.dungeons.append(dungeon)
                    case "felvetel gyujtemenybe":
                        card = findByName(controller.world.cards, command[1])
                        controller.world.collection.append(replace(card))
                    case "uj pakli":
                        controller.createDeck(command[1].split(","))
                    case "harc":
                        dun = findByName(controller.world.dungeons, command[1])
                        if controller.canVisitBigDungeon == False and dun.dungeon_type is DungeonType.BIG:
                            continue
                        controller.fight_system.prepare(controller.deck, dun)
                        with open(WORKDIR.joinpath(command[2]), "a") as file:
                            file.write(f"harc kezdodik;{command[1]}\n\n")
                            res = ""
                            while not res.startswith("jatekos"):
                                res = controller.fight_system.iterate()
                                file.write(res)
                                file.write("\n")
                                if "jatekos;" in res:
                                    file.write("\n")
                            
                    case "export vilag":
                        with open(WORKDIR.joinpath(command[1]), "a") as file:
                            for card in controller.world.cards:
                                name = card.name
                                damage = card.damage
                                health = card.health
                                match(card.element):
                                    case Element.FIRE:
                                        element = "tuz"
                                    case Element.WATER:
                                        element = "viz"
                                    case Element.EARTH:
                                        element = "fold"
                                    case Element.AIR:
                                        element = "levego"
                                file.write(f"kartya;{name};{damage};{health};{element}\n")

                            file.write("\n")
                            for leader in controller.world.leaders:
                                name = leader.name
                                damage = leader.damage
                                health = leader.health
                                match(leader.element):
                                    case Element.FIRE:
                                        element = "tuz"
                                    case Element.WATER:
                                        element = "viz"
                                    case Element.EARTH:
                                        element = "fold"
                                    case Element.AIR:
                                        element = "levego"
                                file.write(f"vezer;{name};{damage};{health};{element}\n")

                            file.write("\n")
                            for dungeon in controller.world.dungeons:
                                name = dungeon.name
                                dun_type = dungeon.dungeon_type.value
                                reward = dungeon.reward.value
                                cards = "".join([f"{card.name}," for card in dungeon.cards])[:-1]
                                leader = f";{dungeon.leader.name}" if dungeon.leader is not None else ""
                                file.write(f"kazamata;{dun_type};{name};{cards}{leader}{reward}\n")

                    case "export jatekos":
                        with open(WORKDIR.joinpath(command[1]), "a") as file:
                            for card in controller.world.collection:
                                name = card.name
                                damage = card.damage
                                health = card.health
                                match(card.element):
                                    case Element.FIRE:
                                        element = "tuz"
                                    case Element.WATER:
                                        element = "viz"
                                    case Element.EARTH:
                                        element = "fold"
                                    case Element.AIR:
                                        element = "levego"
                                file.write(f"gyujtemeny;{name};{damage};{health};{element}\n")
                        
                            for card in controller.deck:
                                file.write(f"\npakli;{card.name}")
            except Exception as e:
                print(e)