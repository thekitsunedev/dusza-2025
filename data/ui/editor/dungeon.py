from string import ascii_letters, digits
import pygame
import pygame_menu

class DungeonCreator:
    def __init__(self, world, update):
        self.world = world
        self.update = update

        self.dungeon = {
            "name": "",
            "type": 0,  # 0: simple, 1: small, 2: big
            "reward": 0, # 0: Health, 1: damage, 2: card
            "cards": [],
            "leader": ""
        }

        # Menu
        self.menu = pygame_menu.Menu(
            title="",
            width=1920//3*2,
            height=1080,
            position=(1920//3, 0, 0),
            theme=pygame_menu.themes.THEME_DARK
        )

        # Dungeon selector
        self.dungeon_selector = self.menu.add.dropselect(
            title="Kazamata",
            items=[("Új", 0)],
            default=0,
            dropselect_id="dungeon_selector",
            onchange=self.onDungeonSelected
        )

        # Name input
        self.dungeon_name = self.menu.add.text_input(
            title="Név ",
            default="",
            onchange=self.onNameChanged,
            textinput_id="dungeon_name",
            valid_chars=list(ascii_letters) + list(digits) + [' ', '-', '_', "'"],
            maxchar=20
        )

        # Type selector
        self.dungeon_type = self.menu.add.dropselect(
            title="Típus",
            items=[("Egyszerű", 0), ("Kis", 1), ("Nagy", 2)],
            default=0,
            onchange=self.onTypeSelected,
            dropselect_id="dungeon_type"
        )

        # Reward selector
        self.dungeon_reward = self.menu.add.dropselect(
            title="Nyeremény",
            items=[("Életerő", 0), ("Sebzés", 1)],
            default=0,
            onchange=self.onRewardSelected,
            dropselect_id="dungeon_reward"
        )

        # Card selector
        self.dungeon_cards = self.menu.add.dropselect_multiple(
            title="Kártyák",
            items=[("", 0)],
            default=None,
            dropselect_multiple_id="dungeon_cards",
            max_selected=1,
            onchange=self.onCardSelected
        )
        self.dungeon_cards.readonly = True

        # Leader selector
        self.dungeon_leader = self.menu.add.dropselect(
            title="Vezér",
            items=[("Nincs vezér", 0)],
            default=0,
            dropselect_id="dungeon_leader",
            onchange=self.onLeaderSelected
        )
        self.dungeon_leader.readonly = True

        # Buttons
        self.menu.add.button(
            title="Hozzáadás",
            action=self.storeDungeon
        )
        self.menu.add.button(
            title="Törlés",
            action=self.deleteDungeon
        )

    ### Runtime
    def draw(self, ctx):
        self.menu.draw(ctx.screen)
    
    def eventHandler(self, events):
        self.menu.update(events)
    
    def updateContent(self, world):
        self.world = world
        print(self.world["dungeons"])
        # Load dungeons
        dungeons = [("Új", 0)]
        for i, dungeon in enumerate(self.world["dungeons"], 1):
            dungeons.append((dungeon, i))
        print(dungeons)
        self.dungeon_selector.update_items(dungeons)
        self.dungeon_selector.set_value(0)

        # Load cards
        cards = []
        for i, card in enumerate(self.world["cards"], 1):
            cards.append((card, i))
        
        self.dungeon_cards.readonly = False
        if len(cards) == 0:
            cards.append(("", 0))
            self.dungeon_cards.readonly = True

        self.dungeon_cards.update_items(cards)
        self.dungeon_cards.reset_value()

        # Load leaders
        leaders = [("Nincs", 1)]
        for i, leader in enumerate(self.world["leaders"], 1):
            leaders.append((leader, i))
        self.dungeon_leader.readonly = len(leaders) == 1
        self.dungeon_leader.update_items(leaders)
        self.dungeon_leader.set_value(0)

        self.reset() # Just to be safe
    
    def reset(self):
        # Name
        self.dungeon_name.set_value("")
        self.dungeon_name.readonly = False

        # Type
        self.dungeon_type.set_value(0)

        # Reward
        self.dungeon_reward.update_items([("Életerő", 0), ("Sebzés", 1)])
        self.dungeon_reward.set_value(0)

        # Cards
        self.dungeon_cards.set_default_value([])
        self.dungeon_cards._make_selection_drop()

    ### Event handlers
    def onDungeonSelected(self, value, index):
        # Reset
        if index == 0:
            self.reset()
        else:
            self.dungeon["name"] = value[0][0]
            dun = self.world["dungeons"][self.dungeon["name"]]
            self.dungeon["type"] = {"SIMPLE": 0, "SMALL": 1, "BIG": 2}[dun.get("type", 0)]
            self.dungeon["reward"] = {"HEALTH": 0, "DAMAGE": 1, "CARD": 2}[dun.get("reward", 0)]
            self.dungeon["cards"] = dun.get("cards", [])
            self.dungeon["leader"] = dun.get("leader", "")

            # Name
            self.dungeon_name.set_value(self.dungeon["name"])
            self.dungeon_name.readonly = True

            # Type
            self.dungeon_type.set_value(self.dungeon["type"])

            # Reward
            self.dungeon_reward.readonly = self.dungeon["type"] == 2
            if self.dungeon["type"] == 2:
                self.dungeon_reward.update_items([("Kártya", 2)])
                self.dungeon_reward.set_value(0)
            else:
                self.dungeon_reward.update_items([("Életerő", 0), ("Sebzés", 1)])
                self.dungeon_reward.set_value(self.dungeon["reward"])
            
            # Cards
            max_selected = {0: 1, 1: 3, 2: 5}[self.dungeon["type"]]
            cards = self.dungeon_cards.get_items()
            selection = [card[1]-1 for card in cards if card[0] in self.dungeon["cards"]][:max_selected]
            print(selection)
            self.dungeon_cards.set_default_value(selection)
            self.dungeon_cards._make_selection_drop()
            self.dungeon_cards._max_selected = max_selected
            self.dungeon_cards.reset_value()

            # Leader
            self.dungeon_leader.readonly = self.dungeon["type"] == 0
            self.dungeon_leader.set_value(0)
            if self.dungeon["type"] != 0:
                for leader in self.dungeon_leader.get_items()[1:]:
                    if self.dungeon["leader"] == leader[0]:
                        self.dungeon_leader.set_value(leader[1])
                        break

    def onNameChanged(self, value):
        self.dungeon["name"] = value
    
    def onTypeSelected(self, value, index):
        self.dungeon["type"] = index
        # Limit card options
        self.dungeon_cards._max_selected = {0: 1, 1: 3, 2: 5}[index]

        # Limit leaders
        self.dungeon_leader.readonly = index == 0
        if index == 0:
            self.dungeon["leader"] = ""
            self.dungeon_leader.set_value(0)
        
        # Set reward type
        self.dungeon_reward.readonly = index == 2
        if index == 2:
            self.dungeon["reward"] = 2
            self.dungeon_reward.update_items([("Kártya", 2)])
            self.dungeon_reward.set_value(0)
        else:
            self.dungeon["reward"] = 0
            self.dungeon_reward.update_items([("Életerő", 0), ("Sebzés", 1)])
            self.dungeon_reward.set_value(0)
    
    def onRewardSelected(self, value, index):
        self.dungeon["reward"] = index
    
    def onCardSelected(self, value):
        self.dungeon["cards"] = [card[0] for card in value[0]]
    
    def onLeaderSelected(self, value, index):
        self.dungeon["leader"] = value[0][0]
    
    def storeDungeon(self):
        dun_type = {0: "SIMPLE", 1: "SMALL", 2: "BIG"}[self.dungeon["type"]]
        dun_reward = {0: "HEALTH", 1: "DAMAGE", 2: "CARD"}[self.dungeon["reward"]]
        self.world["dungeons"][self.dungeon["name"]] = {
            "type": dun_type,
            "reward": dun_reward,
            "leader": self.dungeon["leader"],
            "cards": self.dungeon["cards"]
        }
        self.update(self.world)
    
    def deleteDungeon(self):
        self.world["dungeons"].pop(self.dungeon["name"])

        self.update(self.world)