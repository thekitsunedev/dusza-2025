from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Center, Grid, Vertical
from textual.widgets import Button, Footer, Static
from textual.screen import Screen
from textual.containers import Container
import data.prototypes.controller as controller
from data.ui.card import Kazamatak, Vilagkartyak, Gyujtemenyek
from data.ui.title import Title
from data.ui.createdeck import SelectionScreen



class MainMenu(Screen):
    def compose(self):
        with Vertical():
            yield Static("Üdvözöllek a Damareenben!", id="title")
            with Horizontal():
                yield Button("Világkártyák", id="vilagkartyak", classes="button-row")
                yield Button("Kazamaták", id="kazamatak",  classes="button-row")
                yield Button("Gyűjtemény", id="gyujtemeny",  classes="button-row")
                yield Button("Kilépés", id="kilepesgomb")
                yield Button("Harc", id="harcgomb", classes="button-row")
            

    def on_button_pressed(self, event: Button.Pressed):
            button_id = event.button.id

            if button_id == "vilagkartyak":
                self.app.push_screen(VilagScreen())
            elif button_id == "kazamatak":
                self.app.push_screen(KazamatakScreen())
            elif button_id == "kilepesgomb":
                self.app.exit()
            elif button_id == "gyujtemeny":
                self.app.push_screen(GyujtemenyScreen())
            elif button_id == "harcgomb":
                self.app.push_screen(SelectionScreen())

class VilagScreen(Screen):
    def compose(self):
        yield Title("Világkártyák")
        yield Button("Vissza", id="visszagomb")
        with Grid(id="vilag_grid"):
            for i in controller.game_cards:
                yield Vilagkartyak(i)
    DEFAULT_CSS = """
        #vilag_grid{
            grid-size:8;
            grid-gutter:0;
            width: 100% 
        }
        """
    def on_button_pressed(self, event: Button.Pressed):
        button_id = event.button.id
        if button_id == "visszagomb":
            self.app.push_screen(MainMenu())
        else: self.app.exit()


class KazamatakScreen(Screen):
    
    def compose(self):
        yield Title("Kazamaták")
        yield Button("Vissza", id="visszagomb")
        with Horizontal():    
            for i in controller.dungeons:
                yield Kazamatak(i)

    def on_button_pressed(self, event: Button.Pressed):
        button_id = event.button.id
        if button_id == "visszagomb":  
            self.app.push_screen(MainMenu())
        else: self.exit()

class GyujtemenyScreen(Screen):
    
    def compose(self):
        yield Title("Gyűjtemény")
        yield Button("Vissza", id="visszagomb")
        with Grid(id="dungeon_grid"):
            for i in controller.collection:
                 yield Gyujtemenyek(i)

    DEFAULT_CSS ="""
    #dungeon_grid{
        grid-size:5;
        grid-gutter:6
    }
    """

    def on_button_pressed(self, event: Button.Pressed):
        button_id = event.button.id
        if button_id == "visszagomb":
            
            self.app.push_screen(MainMenu())

          





class GameStart(App):
    SCREENS = {
        "main": MainMenu
        
    }
    CSS_PATH = "css.tcss"
    def on_mount(self):
         self.push_screen("main")

            
def init():
    app = GameStart()
    app.run()