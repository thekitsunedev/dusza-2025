from textual.widgets import Button


class CardButton(Button):
    def __init__(self, card_name, label=None, variant="default", *, name=None, id=None, classes=None, disabled=False, tooltip=None, action=None, compact=False, flat=False):
        if "#" in card_name and "." in card_name:
            id_part = card_name.split("#")[1].split(".")[0]
            clean_label = id_part.replace("card_", "")
        else:
            clean_label = card_name  

        super().__init__(clean_label, variant, name=name, id=id, classes=classes, disabled=disabled, tooltip=tooltip, action=action, compact=compact, flat=flat)
        self.card_name = clean_label
        self.selected = False

    def Toggle(self):
        self.selected = not self.selected
        self.set_class(self.selected, "-selected")
