from textual.app import App, ComposeResult
from textual.containers import Horizontal, Center
from textual.widgets import Placeholder
from textual.widgets import Button, Footer, Static
from textual.containers import Container, Middle
import data.prototypes.controller as controller

class Kazamatak(Container):
    def __init__(self, Kazamata, *children, name = None, id = None, classes = None, disabled = False, markup = True):
          super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
          self.Kazamata = Kazamata
          self.rewardmask = {
               "HEALTH": "+2 Életerő",
               "STRENGTH": "+1 Sebzés",
               "CARD": "+1 Kártya"



          }
    def compose(self):
            yield Static(self.Kazamata.name)
            yield Static(self.rewardmask[self.Kazamata.reward.name])
    DEFAULT_CSS = """
        Kazamatak {
            width: 20;
            height: 8;
            border: round white;
            padding: 1;
            margin: 1;
            margin-left: 30;
        }
        Static{
            color: red;
            content-align: center middle;
            text-style: italic;
        }
"""

class Vilagkartyak(Container):
    def __init__(self, Vilagkartya, *children, name = None, id = None, classes = None, disabled = False, markup = True):
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
        self.Vilagkartya = Vilagkartya
        self.LOCALE_MASK: dict = {
            "EARTH": "Föld",
            "WATER": "Víz",
            "FIRE": "Tűz",
            "AIR": "Levegő"
  }
    def compose(self):
         yield Static(self.Vilagkartya.name)
         yield Static(str(self.Vilagkartya.strength) + "/" + str(self.Vilagkartya.health))
         yield Static(self.LOCALE_MASK[self.Vilagkartya.element.name])
    DEFAULT_CSS = """
        Vilagkartyak {
            width: 20;
            height: 7;
            border: round white;
            padding: 1;
            margin: 1;
            margin-top: 10;
            align-horizontal: center;
        
        }
        Static{
            color: rgba(5, 145, 145, 1);
            content-align: center middle;
        
        }
"""

class Gyujtemenyek(Container):
    def __init__(self, Gyujtemeny,*children, name = None, id = None, classes = None, disabled = False, markup = True):
          super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
          self.Gyujtemeny = Gyujtemeny
          self.localemasks = {
               "EARTH": "Föld",
               "WATER": "Víz",
               "FIRE": "Tűz",
               "AIR": "Levegő"
          }
    def compose(self):
         yield Static(self.Gyujtemeny.name)
         yield Static(str(self.Gyujtemeny.strength)+"/"+str(self.Gyujtemeny.health))
         yield Static(self.localemasks[self.Gyujtemeny.element.name])
    DEFAULT_CSS = """
            Gyujtemenyek {
            width: 40;
            height: 8;
            border: round white;
            padding: 1;
            margin: 1;
        
        }
        Static{
            color: rgba(5, 145, 145, 1);
            content-align: center middle;
        
        }



"""
class KazamataKartyak(Container):
    def __init__(self, Kazamatakartya,*children, name = None, id = None, classes = None, disabled = False, markup = True):
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
        self.Kazamatakartya = Kazamatakartya
        self.localemasks = {
               "EARTH": "Föld",
               "WATER": "Víz",
               "FIRE": "Tűz",
               "AIR": "Levegő"
          }
    
    def compose(self):
         yield Static(self.Kazamatakartya.name)
         yield Static(str(self.Kazamatakartya.strength) + "/" + str(self.Vilagkartya.health))
         yield Static(self.localemasks[self.Kazamatakartya.element.name])

    DEFAULT_CSS = """
        Gyujtemenyek {
        width: 40;
        height: 8;
        border: round white;
        padding: 1;
        margin: 1;
        
        }
        Static{
        color: rgba(5, 145, 145, 1);
        content-align: center middle;
        
        }
        """