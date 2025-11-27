from math import ceil
from os import remove
from json import load, dump
from string import ascii_letters, digits
from pathlib import Path
import pygame
import pygame_menu



PATH = Path(__file__).resolve().parent.parent.parent.joinpath("custom_worlds")

class WorldCreator:
    def __init__(self, world):
        self.world = world
        self.world_name = ""
        self.menu = pygame_menu.Menu("", width=1920//3*2, height=1080,
                                    position=(1920//3, 0, 0), theme=pygame_menu.themes.THEME_DARK)
        self.worlds = []
        self.getWorlds()
        self.menu.add.dropselect(
            title="Világ",
            items=self.worlds,
            onchange=self.onWorldSelect,
            dropselect_id="selector",
            default=0
        )

        self.menu.add.text_input(
            title="Világnév ",
            textinput_id="world_name",
            maxchar=20,
            onchange=self.onWorldNameChange,
            valid_chars=list(ascii_letters) + list(digits) + [" ", "_", "-"],

        )
        
        self.menu.add.range_slider(
            title="Nehézség",
            default=0,
            range_values=(0.0, 10.0),
            increment=1.0,
            value_format=lambda x: f"{x:.0f}",
            onchange=self.setDifficulty,
            rangeslider_id="difficulty"
        )

        ds = self.menu.add.dropselect_multiple(
            title="Gyűjtemény",
            dropselect_multiple_id="collection",
            items=[("", "")],
            default=[],
            max_selected=0,
            onchange=self.onCollectionChange
        )
        ds.reset_value()

        self.menu.add.button(
            title="Mentés",
            action=self.saveWorld
        )
        self.menu.add.button(
            title="Törlés",
            action=self.deleteWorld
        )
    
    def draw(self, ctx):
        self.menu.get_widget("collection").readonly = len(self.world["cards"].keys()) == 0

        self.menu.draw(ctx.screen)
            
    
    def eventHandler(self, event):
        self.menu.update(event)

    def getWorlds(self):
        self.worlds.clear()
        self.worlds.append(("Új", 0))
        for file in PATH.glob("*"):
            name = file.parts[-1]
            if not name.endswith(".json"):
                continue
            self.worlds.append((name.split(".")[0], name))
    

    def onWorldSelect(self, value, index):
        self.world.clear()
        self.world["difficulty"] = 0
        self.world["cards"] = {}
        self.world["leaders"] = {}
        self.world["dungeons"] = {}
        self.world["collection"] = []
        name = value[0][1]
        wname = self.menu.get_widget("world_name")

        if name == 0:
            wname.readonly = False
            wname.set_value("")
            self.updateCollectionList()
            return
        self.world_name = value[0][0]
        with open(PATH.joinpath(name)) as file:
            self.world = load(file)
        
        difficulty = self.menu.get_widget("difficulty").set_value(self.world["difficulty"])
        wname.set_value(value[0][0])
        wname.readonly = True
        self.updateCollectionList()
    
    def onWorldNameChange(self, value):
        self.world_name = value
    
    def saveWorld(self):
        with open(PATH.joinpath(f"{self.world_name}.json"), "w") as file:
            dump(self.world, file)
        self.getWorlds()
        self.menu.get_widget("selector").update_items(self.worlds)
        self.menu.get_widget("selector").set_value(self.world_name)
    
    def deleteWorld(self): 
        self.world.clear()
        self.world["difficulty"] = 0
        self.world["cards"] = {}
        self.world["leaders"] = {}
        self.world["dungeons"] = {}
        self.world["collection"] = []
        try:
            remove(PATH.joinpath(f"{self.world_name}.json"))
        except:
            ...
        self.getWorlds()
        self.menu.get_widget("selector").update_items(self.worlds)
        self.menu.get_widget("selector").set_value("Új")
    
    def setDifficulty(self, value):
        self.world["difficulty"] = int(value)

    
    def updateCollectionList(self):
        ds = self.menu.get_widget("collection")
        options = []
        default = []

        cards = self.world["cards"]
        if len(cards.keys()) == 0:
            options = [("", 0)]
        else:
            for i, card in enumerate(cards):
                options.append((card, i))
                if card in self.world["collection"]:
                    default.append(i)

        ds._max_selected = ceil(len(options) / 2)
        ds.update_items(options)
        ds.set_default_value(default)
        ds._make_selection_drop()
        ds.reset_value()
    
    def onCollectionChange(self, value):
        self.world["collection"] = [card[0] for card in value[0]]