import pygame
import pygame_menu
from data.ui.navigator import Scene, Navigator
from data.ui.objects import Context

class SaveSelect(Scene):
    def __init__(self, name):
        super().__init__(name)
        self.save_name = ""
    
    def run(self, ctx: Context, nav: Navigator):
        self.ctx = ctx
        self.nav = nav
        menu = pygame_menu.Menu(
            title = "",
            width=1920,
            height=1080,
            theme=pygame_menu.themes.THEME_DARK
        )

        saves = ctx.conn.fetchSaves()

        if len(saves) == 0:
            menu.add.label("Nem található mentés")

            # New game
            menu.add.button(
                title="Új játék",
                action=lambda: nav.navigate("WorldSelect")
            )

        else:
            saves = [(save, i) for i, save in enumerate(saves)]
            menu.add.dropselect(
                title="Mentés",
                items=saves,
                onchange=self.selectSave,
                placeholder="Válasz mentést"
            )

            # Load save
            menu.add.button(
                title="Betöltés",
                action=self.loadSave
            )

            # Delete save
            menu.add.button(
                title="Törlés",
                action=self.deleteSave
            )
        
        # Back to main menu
        menu.add.button(
            title="Vissza",
            action=lambda: nav.navigate("Starter")
        )

        while nav.running:
            ctx.screen.fill("#7f7f7f")
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    nav.navigate("QUIT")
                    return
            if menu.is_enabled():
                menu.update(events)
                menu.draw(ctx.screen)
            pygame.display.update()
    
    save_name = ""
    def loadSave(self):
        if self.save_name == "":
            return
        self.ctx.conn.loadSave(self.save_name)
        self.nav.navigate("MainMenu")
        
    def deleteSave(self):
        if self.save_name == "":
            return
        self.ctx.conn.deleteSave(self.save_name)
        
    def selectSave(self, value, index):
        self.save_name = value[0][0]
