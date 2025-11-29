from string import ascii_letters, digits
import pygame
import pygame_menu

class CardCreator:
    def __init__(self, world, update):
        self.update = update
        self.world = world
        self.card_name = ""
        self.health = 1
        self.damage = 2
        self.element = 0
        self.menu = pygame_menu.Menu("", width=1920//3*2, height=1080,
                                    position=(1920//3, 0, 0), theme=pygame_menu.themes.THEME_DARK)
        
        self.menu.add.dropselect(
            title="Kártya",
            items=[("Új", 0)],
            default=0,
            dropselect_id="card_selector",
            onchange=self.onCardSelected
        )
        self.menu.add.text_input(
            title="Név ",
            textinput_id="card_name",
            maxchar=16,
            onchange=self.onCardNameChange,
            valid_chars=list(ascii_letters) + list(digits) + [" ", "_", "-", "'"],
        )
        self.menu.add.range_slider(
            title="Sebzés",
            default=2.0,
            range_values=(2.0, 100.0),
            increment=1.0,
            value_format=lambda x: f"{x:.0f}",
            onchange=self.onDamageChanged,
            rangeslider_id="damage_slider"
        )
        self.menu.add.range_slider(
            title="Életerő",
            default=1.0,
            range_values=(1.0, 100.0),
            increment=1.0,
            value_format=lambda x: f"{x:.0f}",
            onchange=self.onHealthChanged,
            rangeslider_id="health_slider"
        )
        self.menu.add.dropselect(
            title="Típus",
            items=[("Tűz", 0), ("Viz", 1), ("Levegő", 2), ("Föld", 3)],
            dropselect_id="element_selector",
            onchange=self.onElementChanged,
            default=0
        )
        self.menu.add.button(
            title="Hozzáadás",
            action=self.createCard
        )
        self.menu.add.button(
            title="Törlés",
            action=self.deleteCard
        )
    
    def draw(self, ctx):
        self.menu.draw(ctx.screen)
    
    def eventHandler(self, event):
        self.menu.update(event)
    
    def onCardSelected(self, value, index):
        self.card_name = value[0][0]
        self.card = self.world["cards"].get(self.card_name, {})
        if self.card_name == "Új":
            disp = ""
        else:
            disp = self.card_name
        self.menu.get_widget("card_name").set_value(disp)
        self.menu.get_widget("damage_slider").set_value(self.card.get("damage", 2))
        self.menu.get_widget("health_slider").set_value(self.card.get("health", 1))
        self.menu.get_widget("element_selector").set_value({"FIRE": 0, "WATER": 1, "AIR": 2, "EARTH": 3, 0: 0}[self.card.get("element", 0)])

    def onCardNameChange(self, value):
        self.card_name = value
    
    def onDamageChanged(self, value):
        self.damage = round(value)
    
    def onHealthChanged(self, value):
        self.health = round(value)
    
    def onElementChanged(self, value, index):
        self.element = index
    
    def createCard(self):
        self.world["cards"][self.card_name] = {
            "damage": self.damage,
            "health": self.health,
            "element": ["FIRE","WATER","AIR","EARTH"][self.element]
        }
        self.update(self.world)
    
    def deleteCard(self):
        self.world["cards"].pop(self.card_name)
        self.update(self.world)


    def updateContent(self, world):
        self.world = world
        options = [("Új", 0)]
        for i, card in enumerate(self.world["cards"].keys(), 1):
            options.append((card, i))
        self.menu.get_widget("card_selector").update_items(options)
        self.menu.get_widget("card_selector").set_value(0)