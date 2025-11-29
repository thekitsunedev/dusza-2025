import pygame
from data.uiprototype.navigator import Scene, Navigator
from data.uiprototype.objects import Context
from .world import WorldCreator
from .card import CardCreator
from .leader import LeaderCreator
from .dungeon import DungeonCreator

class Editor(Scene):
    def __init__(self, name):
        super().__init__(name)

        # Styling
        self.BG_COLOR = (127, 127, 127)
        self.FONT_COLOR = (255, 255, 255)
        self.BUTTON_COLOR = (25, 25, 25)
        self.BUTTON_HOVER = (100, 100, 100)
        self.BUTTON_SELECTED = (75, 75, 75)

        self.world: dict = {}
        self.world["difficulty"] = 0
        self.world["cards"] = {}
        self.world["leaders"] = {}
        self.world["dungeons"] = {}
        self.world["collection"] = []
        self.PAGE = {
            "world": WorldCreator(self.world, self.update),
            "cards": CardCreator(self.world, self.update),
            "leaders": LeaderCreator(self.world, self.update),
            "dungeons": DungeonCreator(self.world, self.update)
        }
        self.LOCALE = {
            "world": "Világ",
            "cards": "Kártyák",
            "leaders": "Vezérek",
            "dungeons": "Kazamaták",
            "back": "Vissza"
        }

    
    def run(self, ctx: Context, nav: Navigator) -> None:
        self.selected = "world"
        while nav.running:
            ctx.screen.fill(self.BG_COLOR)
            maus = pygame.mouse.get_pos()

            # Draw buttons
            buttons: dict = {}
            offset = 5
            for button in self.LOCALE.keys():
                text = ctx.font.render(self.LOCALE.get(button), True, self.FONT_COLOR)
                rect = text.get_rect()
                rect.y = offset
                rect.x = 10
                offset += rect.height + 15

                if button == "back":
                    rect.y = 1080 - 5 - rect.height

                box = pygame.Rect(
                    rect.x - 10, rect.y - 5,
                    rect.width + 20, rect.height + 10
                )

                background = self.BUTTON_COLOR
                if box.collidepoint(maus):
                    background = self.BUTTON_HOVER
                if self.selected == button:
                    background = self.BUTTON_SELECTED

                pygame.draw.rect(ctx.screen, background, box)
                ctx.screen.blit(text, rect)

                buttons[button] = box


            # Load editor pages
            self.PAGE.get(self.selected).draw(ctx)

            pygame.display.update()
            # Handle quit requests, and button presses
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    nav.navigate("QUIT")
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons.keys():
                        box = buttons.get(button)
                        if box.collidepoint(event.pos):
                            if button == "back":
                                nav.navigate("MainMenu")
                                return
                            else:
                                self.selected = button
                
                # Event listener
            for page in self.PAGE.keys():
                if self.selected == page:
                    self.PAGE[page].eventHandler(events)
    
    def update(self, world):
        self.world = world
        for page in self.PAGE:
            self.PAGE[page].updateContent(self.world)