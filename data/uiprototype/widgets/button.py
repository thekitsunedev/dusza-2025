import pygame

class Button:
    def __init__(self, text, position: tuple[int], handler = None, **options):
        """
        text: str
        size: tuple (x, y),
        handler: function
        style:
            bg_color: (50, 50, 50)
            bg_hover: (100, 100, 100)
            bg_active: (75, 75, 75)
            bg_disabled: (25, 25, 25)
            color: (255, 255, 255)
            font_type: 1 (80px)! | 2 (20px)
        options:
            disabled: False
            toggle: False
        """
        # Styling
        self.bg_color: tuple[int] = options.get("bg_color", (25, 25, 25))
        self.bg_hover: tuple[int] = options.get("bg_hover", (100, 100, 100))
        self.bg_selected: tuple[int] = options.get("bg_active", (75, 75, 75))
        self.bg_disabled: tuple[int] = options.get("bg_disabled", (50, 50, 50))
        self.text_color: tuple[int] = options.get("color", (255, 255, 255))
        self.font_type: int = min(max(options.get("font_type", 1), 1), 2)
        
        # Options
        self.disabled: bool = options.get("disabled", False)
        self.toggle: bool = options.get("toggle", False)
        
        # Callback
        self.handler = handler or (lambda: None)
    
        self._state = False
        self.text = text
        self.position = position


    def draw(self, ctx):
        if self.font_type == 1:
            font = ctx.font
        elif self.font_type == 2:
            font = ctx.font2
        
        text = font.render(self.text, True, self.text_color)
        rect = text.get_rect()
        rect.x = self.position[0]
        rect.y = self.position[1]

        self.box = pygame.Rect(
            rect.x - 10, rect.y - 5,
            rect.width + 20, rect.height + 10
        )

        maus = pygame.mouse.get_pos()
        if self.disabled:
            background = self.bg_disabled
        elif self.box.collidepoint(maus):
            background = self.bg_hover
        elif self._state and self.toggle:
            background = self.bg_selected
        else:
            background = self.bg_color
        pygame.draw.rect(ctx.screen, background, self.box)
        ctx.screen.blit(text, rect)

    def think(self, event):
        if self.disabled:
            return

        if self.box is None:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.box.collidepoint(event.pos):
                if self.toggle:
                    self._state = not self._state
                    self.handler(state=self._state)
                else:
                    self.handler()


    @property
    def state(self) -> bool:
        return self._state