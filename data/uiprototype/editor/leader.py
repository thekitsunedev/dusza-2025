from string import ascii_letters, digits
import pygame
import pygame_menu

class LeaderCreator:
    def __init__(self, world, update):
        self.world = world
        self.update = update
        self.leader_name = ""
        self.buff = 0
        self.inherit_name = ""
        self.menu = pygame_menu.Menu("", width=1920//3*2, height=1080,
                                    position=(1920//3, 0, 0), theme=pygame_menu.themes.THEME_DARK)
        
        self.menu.add.dropselect(
            title="Vezért",
            items=[("Új", 0)],
            default=0,
            dropselect_id="leader_selector",
            onchange=self.onLeaderSelected
        )
        self.menu.add.text_input(
            title="Név ",
            textinput_id="leader_name",
            maxchar=16,
            onchange=self.onLeaderNameChange,
            valid_chars=list(ascii_letters) + list(digits) + [" ", "_", "-", "'"]
        )
        self.menu.add.dropselect(
            title="Kártya",
            items=[("", 0)],
            default=0,
            dropselect_id="card_selector",
            onchange=self.onCardSelected
        )
        self.menu.add.dropselect(
            title="Dupláz",
            items=[("Életerő", 0), ("Sebzés", 1)],
            default=0,
            onchange=self.onInheritSelected,
            dropselect_id="inherit_selector"
        )
        self.menu.add.button(
            title="Hozzáadás",
            action=self.addLeader
        )
        self.menu.add.button(
            title="Törlés",
            action=self.deleteLeader
        )
    
    def draw(self, ctx):
        self.menu.draw(ctx.screen)
    
    def eventHandler(self, event):
        self.menu.update(event)
    
    def updateContent(self, world):
        self.world = world
        options = [("Új", 0)]
        for i, card in enumerate(self.world["leaders"].keys(), 1):
            options.append((card, i))
        self.menu.get_widget("leader_selector").update_items(options)
        self.menu.get_widget("leader_selector").set_value(0)


        if len(self.world["cards"]) == 0:
            self.menu.get_widget("card_selector").readonly = True
            return
        self.menu.get_widget("card_selector").readonly = False
        options = []
        for i, card in enumerate(self.world["cards"].keys()):
            options.append((card, i))
        self.menu.get_widget("card_selector").update_items(options)
    
    def onLeaderSelected(self, value, index):
        if value[0][0] == "Új":
            self.menu.get_widget("leader_name").set_value("")
            self.menu.get_widget("inherit_selector").set_value(0)
        else:
            self.menu.get_widget("leader_name").set_value(value[0][0])
            self.leader_name = value[0][0]
            self.menu.get_widget("inherit_selector").set_value(
                0 if self.world["leaders"][self.leader_name] == "HEALTH" else 1
            )
            self.menu.get_widget("card_selector").set_value(
                self.world["leaders"][self.leader_name]["inherit"]
            )
        

    
    def onLeaderNameChange(self, value):
        self.leader_name = value
    
    def onCardSelected(self, value, index):
        self.inherit_name = value[0][0]
    
    def onInheritSelected(self, value, index):
        self.buff = index
    
    def addLeader(self):
        self.world["leaders"][self.leader_name] = {
            "inherit": self.inherit_name,
            "buff": "DAMAGE" if self.buff == 1 else "HEALTH",
        }
        self.update(self.world)
    
    def deleteLeader(self):
        self.world["leaders"].pop(self.leader_name)
        self.update(self.world)    