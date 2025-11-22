from pathlib import Path
from data.prototypes.controller import Controller
import data.prototypes.parser.save as save



class WorldCalls:
    def __init__(self):
        super().__init__()


    def fetchWorlds(self) -> list:
        """
        Returns the world names in a list.
        """
        worlds = []
        worlds.append("default_world")
        for file in self.DATA_PATH.joinpath("custom_worlds").glob("*"):
            file_name = file.parts[-1]
            # Skip non-JSON files
            if not file_name.endswith(".json"):
                continue

            worlds.append(file_name.split(".")[0])
    
        return worlds

    def fetchSaves(self) -> list:
        """
        Returns the save names in a list.
        """
        saves = []
        for file in self.DATA_PATH.joinpath("saves").glob("*"):
            file_name = file.parts[-1]
            if not file_name.endswith(".json"):
                continue

            saves.append(file_name.split(".")[0])
    
        return saves

    def loadSave(self, save_name: str) -> None:
        """
        Initializes the save, use fetch* to get info about the world
        """
        self.controller = Controller(save_name)

    def loadWorld(self, world_name: str) -> None:
        """
        Initializes the world, use fetch* to get info about the world
        """
        self.controller = Controller(world_name)

    def createSave(self, save_name: str) -> None:
        """
        Save the current game state in to given name
        """
        world = self.controller.world
        save.save(world, save_name)
    
    def deleteSave(self, save_name: str) -> None:
        """
        Delete Save with given name
        """
        for file in self.DATA_PATH.joinpath("saves").glob("*"):
            file_name = file.parts[-1]
            if not file_name.endswith(".json"):
                continue
            if file_name.startswith(save_name):
                file.unlink()