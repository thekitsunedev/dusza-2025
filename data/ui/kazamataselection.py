from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Center, Grid, Vertical
from textual.widgets import Button, Footer, Static
from textual.screen import Screen
from textual.containers import Container
import data.prototypes.controller as controller
from data.ui.card import Kazamatak, Vilagkartyak, Gyujtemenyek
from data.ui.battleboard import Dungeon
from data.ui.title import Title
from data.ui.button import CardButton
from math import ceil
import data.prototypes.fight_system as arena


class KazamataSelection(Screen):


    def compose(self):
        for i in controller.dungeons:
            yield Button(i.name, id=str(i.name.replace(" ", "")))


    def on_button_pressed(self, event:Button.Pressed):
        button = event.button.id

        if button == "BarlangiPortya":
            arena.init("Barlangi Portya", "")
            self.app.push_screen(Dungeon())

        elif button == "OsiSzenthely":
            arena.init("Osi Szenthely", "")
            self.app.push_screen(Dungeon())

        elif button == "Amelysegkiralynoje":
            if controller.canVisitBigDungeon():
                arena.init("A melyseg kiralynoje", "")
                self.app.push_screen(Dungeon())
