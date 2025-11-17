from textual.app import App, ComposeResult
from textual.containers import Horizontal, Center
from textual.widgets import Placeholder
from textual.widgets import Button, Footer, Static
from textual.containers import Container, Middle, Grid
import data.prototypes.controller as controller


class Title(Container):
    def __init__(self, titlename,*children, name = None, id = None, classes = None, disabled = False, markup = True):
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
        self.titlename = titlename
    def compose(self):
        yield Static(str(self.titlename))  #<---title formázása cssben
    DEFAULT_CSS = """   
        Title {
            width: 20;
            height: 8;
            padding: 1;
            margin: 1;
        }
        Static{
            align-horizontal: center;
            color: rgba(68, 174, 11, 1);
            content-align: center middle
        }
"""