from os.path import join
import data.static.global_definitions as GLOB
import data.prototypes.controller as controller
import data.prototypes.exporter as exporter
import data.prototypes.fight_system as arena

def init(path: str) -> None:
    """
    Command processor for test mode.
    arguments:
        path: path of the files
    """
    ELEMENT_MASK: dict = {
            "tuz": GLOB.Elements.FIRE,
            "levego": GLOB.Elements.AIR,
            "viz": GLOB.Elements.WATER,
            "fold": GLOB.Elements.EARTH
        }

    WORK_DIR: str = path
    exporter.WORK_DIR = WORK_DIR
    arena.WORK_DIR = WORK_DIR

    with open(join(WORK_DIR, "in.txt"), "r") as file:
        for line in file:
            command = line.strip().split(";")
            match(command[0]):
                case "uj kartya":
                    """
                    uj kartya;name;strength;health;element
                    """
                    name = command[1]
                    strength = int(command[2])
                    health = int(command[3])
                    element = ELEMENT_MASK[command[4]]
                    controller.createCard(name,
                                         strength,
                                         health,
                                         element)
                case "uj vezer":
                    """
                    uj vezer;name;inherit_from;buff
                    """
                    name = command[1]
                    inherit_from = command[2]
                    buff = GLOB.InheritBuff.HEALTH if command[3] == "eletero" else ""
                    buff = GLOB.InheritBuff.STRENGTH if command[3] == "sebzes" else ""
                    if buff == "":
                        continue
                    controller.createLeader(name,
                                            inherit_from,
                                            buff)
                case "uj kazamata":
                    """
                    uj kazamata;egyszeru;name;card;reward
                    uj kazamata;kis;name;cards,~;leader;reward
                    uj kazamata;nagy;name;cards,~;leader
                    """
                    dtype_str = command[1]
                    name = command[2]
                    dun_type = GLOB.DungeonTypes.SIMPLE if dtype_str == "egyszeru" else None
                    dun_type = GLOB.DungeonTypes.SMALL if dtype_str == "kis" else dun_type
                    dun_type = GLOB.DungeonTypes.BIG if dtype_str == "nagy" else dun_type

                    cards = command[3].split(",")

                    leader = command[-1] if dun_type == GLOB.DungeonTypes.BIG else ""
                    leader = command[-2] if dun_type == GLOB.DungeonTypes.SMALL else ""

                    reward = GLOB.DungeonRewards.CARD if dun_type == GLOB.DungeonTypes.BIG else \
                        GLOB.DungeonRewards.HEALTH if command[-1] == "eletero" else \
                        GLOB.DungeonRewards.STRENGTH if command[-1] == "sebzes" else ""
                                        
                    controller.createDungeon(name, dun_type, reward, cards, leader,)
                case "felvetel gyujtemenybe":
                    """
                    felvetel gyujtemenybe;name
                    """
                    controller.addToCollection(command[1])
                case "uj pakli":
                    """
                    uj pakli;name,~
                    """
                    controller.createDeck(command[1].split(","))
                case "harc":
                    """
                    harc;dungeon_name;outfile
                    """
                    arena.init(command[1], command[2])
                    arena.start()
                case "export vilag":
                    """
                    export vilag;outfile
                    """
                    exporter.exportWorld(command[1])
                case "export jatekos":
                    """
                    export jatekos;outfile
                    """
                    exporter.exportPlayer(command[1])
                