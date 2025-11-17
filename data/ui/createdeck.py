from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Center, Grid, Vertical
from textual.widgets import Button, Footer, Static
from textual.screen import Screen
from textual.containers import Container
import data.prototypes.controller as controller
from data.ui.card import Kazamatak, Vilagkartyak, Gyujtemenyek
from data.ui.title import Title
from data.ui.button import CardButton
from math import ceil
from data.ui.kazamataselection import KazamataSelection





class SelectionScreen(Screen):
    
    def compose(self):
        self.selected_cards = []
        yield Title("Kártyák kiválasztása")
        for card in controller.collection:
            yield CardButton(card.name, id ="card_"+str(card.name), classes="cardbutton")
        yield Button("Tovább", id="nextpage")
    def on_button_pressed(self, event: Button.Pressed):
        button = event.button
        if event.button.id == "nextpage":
            self.app.push_screen(KazamataSelection())
        if isinstance(button, CardButton):
            button.Toggle()
            if button.selected:
                if len(self.selected_cards) >= ceil(len(controller.collection)/2):
                    return
                button.styles.background = "green"
                self.selected_cards.append(button.card_name)
            else:
                try:
                    self.selected_cards.remove(button.card_name)
                except: ...
                button.styles.background = "#121212"
            controller.createDeck(self.selected_cards)



