from string import ascii_letters, digits
import pygame
import pygame_menu

class DungeonCreator:
    def __init__(self, world, update):
        self.world = world
        self.update = update
        self.dungeon_name = ""
        self.dungeon_type = 0
        self.dungeon_reward = 0
        self.card_options = []
        self.cards = []
        self.leader = ""
        self.menu = pygame_menu.Menu("", width=1920//3*2, height=1080,
                                    position=(1920//3, 0, 0), theme=pygame_menu.themes.THEME_DARK)
    
        self.menu.add.dropselect(
            title="Kazamata",
            items=[("Új", 0)],
            default=0,
            dropselect_id="dungeon_selector",
            onchange=self.onDungeonSelected
        )
        self.menu.add.text_input(
            title="Név ",
            default="",
            onchange=self.onDungeonNameChange,
            valid_chars=list(ascii_letters) + list(digits) + [" ", "_", "-", "'"],
            maxchar=20,
            textinput_id="dungeon_name"
        )
        self.menu.add.dropselect(
            title="Típus",
            items=[("Egyszerű", 0), ("Kis", 1), ("Nagy", 2)],
            default=0,
            dropselect_id="type_selector",
            onchange=self.onTypeChange
        )
        self.menu.add.dropselect(
            title="Nyeremény",
            items=[("Sebzés", 1), ("Életerő", 2)],
            default=1,
            dropselect_id="reward_selector",
            onchange=self.onRewardChange
        )
        self.menu.add.dropselect_multiple(
            title="Kártyák",
            items=[("", 0)],
            dropselect_multiple_id="card_selector",
            max_selected=0,
            onchange=self.onCardSelected
        )
        self.menu.add.dropselect(
            title="Vezér",
            items=[("Nincs", 0)],
            default=0,
            dropselect_id="leader_selector",
            onchange=self.onLeaderSelected
        )
        self.menu.add.button(
            title="Hozzáadás",
            action=self.createDungeon
        )
        self.menu.add.button(
            title="Törlés",
            action=self.deleteDungeon
        )

    def draw(self, ctx):
        self.menu.draw(ctx.screen)
    
    def eventHandler(self, event):
        self.menu.update(event)

    def onDungeonSelected(self, value, index):
        rew = self.menu.get_widget("reward_selector")
        if index == 0:
            self.dungeon_name = ""
            self.menu.get_widget("dungeon_name").readonly = False

            self.dungeon_type = 0
            self.menu.get_widget("type_selector").set_value(0)

            rew.readonly = False
            rew.update_items([("Sebzés", 1), ("Életerő", 2)])
            rew.set_value(1)
            self.dungeon_reward = 1
        else:
            self.dungeon_name = value[0][0]
            dungeon = self.world["dungeons"][self.dungeon_name]
            self.menu.get_widget("dungeon_name").readonly = True
            self.dungeon_type = {"SIMPLE": 0, "SMALL": 1, "BIG": 2}[dungeon["type"]]
            self.menu.get_widget("type_selector").set_value(self.dungeon_type)
            if dungeon["type"] == "BIG":
                rew.update_items([("Kártya", 0)])
                rew.set_value(0)
                rew.readonly = True
                self.dungeon_reward = 0
            else:
                self.dungeon_reward = {"DAMAGE": 1, "HEALTH": 2}[dungeon["reward"]]
                rew.readonly = False
                rew.update_items([("Sebzés", 1), ("Életerő", 2)])
                rew.set_value(self.dungeon_reward - 1)
            self.menu.get_widget("reward_selector")
        
            selected = []
            for i, card in enumerate(self.world["cards"]):
                if card in dungeon["cards"]:
                    selected.append(i)
            print(selected)

            cards = self.menu.get_widget("card_selector")
            cards._max_selected = {0: 1, 1: 3, 2: 5}[self.dungeon_type]
            cards.set_default_value(selected)
            cards._make_selection_drop()
            cards.reset_value()
    
    def onDungeonNameChange(self, value):
        self.dungeon_name = value

    def onTypeChange(self, value, index):
        rew = self.menu.get_widget("reward_selector")
        card = self.menu.get_widget("card_selector")
        if index == 2:
            rew.update_items([("Kártya", 0)])
            rew.set_value(0)
            rew.readonly = True
            self.dungeon_reward = 0
            card._max_selected = 5
        else:
            rew.update_items([("Sebzés", 1), ("Életerő", 2)])
            rew.set_value(1)
            rew.readonly = False
            self.dungeon_reward = 1
            card._max_selected = {1: 3, 2: 5}[index]
        card._make_selection_drop()
        card.reset_value()

    def onRewardChange(self, value, index):
        self.dungeon_reward = index
    
    def onCardSelected(self, value):
        self.cards = [card[0] for card in value[0]]
    
    def onLeaderSelected(self, value, index):
        self.leader = value[0][0]
    
    def createDungeon(self):
        self.world["dungeons"][self.dungeon_name] = {
            "reward": ["CARD", "DAMAGE", "HEALTH"][self.dungeon_reward],
            "type": ["SIMPLE", "SMALL", "BIG"][self.dungeon_type],
            "leader": self.leader,
            "cards": self.cards
        }
        self.update(self.world)
    
    def deleteDungeon(self):
        self.world["dungeons"].pop(self.dungeon_name)
        self.update(self.world)

    def updateContent(self, world):
        self.world = world

        # Dungeons
        options = [("Új", 0)]
        for i, dungeon in enumerate(self.world["dungeons"], 1):
            options.append((dungeon, i))
        self.menu.get_widget("dungeon_selector").update_items(options)
        self.menu.get_widget("dungeon_selector").set_value(0)

        # cards
        cards = self.menu.get_widget("card_selector")
        options = []
        for i, card in enumerate(self.world["cards"]):
            options.append((card, i))
        
        self.card_options = options
        cards.update_items(options)
        cards.reset_value()

        # leaders
        options = []
        for i, card in enumerate(self.world["leaders"]):
            options.append((card, i))
        self.menu.get_widget("leader_selector").update_items(options)