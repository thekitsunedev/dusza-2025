from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Center, Grid, Vertical
from textual.widgets import Button, Footer, Static
from textual.screen import Screen
from textual.reactive import Reactive
from textual.containers import Container
import data.prototypes.controller as controller
from data.ui.card import Kazamatak, Vilagkartyak, Gyujtemenyek, KazamataKartyak
from data.ui.title import Title
from data.static.dungeon import DungeonObject
import data.prototypes.fight_system as arena
import data.ui.init as ini
import asyncio

class Dungeon(Screen):
    def compose(self):
        self.iter_result = ""
        with Horizontal(id="content"):
            with Vertical():
                yield Static("Játékos paklija")
                yield Vertical(id="player")
            with Vertical():
                yield Static("Kazamata paklija")
                yield Vertical(id="enemy")

    def on_mount(self):
        self.set_interval(1, self.refreshPage)
        self.refreshPage()

    def refreshPage(self) -> None:
        if self.iter_result.startswith("jatekos"):
            container = self.query_one(Horizontal)
            container.remove()
            match_result = self.iter_result.split(";")
            match(match_result[0]):
                case "jatekos vesztett":
                    status = "Vesztettél!"
                case "jatekos nyert":
                    if match_result[1] in ["sebzes", "eletero"]:
                        status = "Nyertél! Kártyád: " + match_result[2]
                        status += " +2 életerőt szerzett" if match_result[1] == "eletero" else ""
                        status += " +1 sebzést szerzett." if match_result[2] == "sebzes" else ""
                    else:
                        status = "Nyertél! új kártyát szereztél: " + match_result[1]
            self.mount(Vertical(Static(status), Button("Vissza", id="visszagomb"), id="matchveg"))

            #stop advancing
            self.iter_result = "PAUSED"
        elif self.iter_result != "PAUSED":
            player_container = self.query_one("#player", Vertical)
            player_container.remove_children()
            for i, card in enumerate(arena.arena.deck):
                if i == 0:
                    player_container.mount(Vilagkartyak(card, classes="active"))
                else:
                    player_container.mount(Vilagkartyak(card))
        
            enemy_container = self.query_one("#enemy", Vertical)
            enemy_container.remove_children()
            for i, card in enumerate(arena.arena.dungeonDeck):
                if i == 0:
                    enemy_container.mount(Vilagkartyak(card, classes="active"))
                else:
                    enemy_container.mount(Vilagkartyak(card))
            self.iter_result = arena.arena.iterate()

    def on_button_pressed(self, event:Button.Pressed):
        button = event.button.id

        if button == "visszagomb":
            self.app.push_screen(ini.MainMenu())
    
    
    DEFAULT_CSS = """
    #Vertical {
    content-align: center top;
    }
    .active {
    border: round red;
    }
    #matchveg {
        content-align: center middle;
    }
    """