import pygame
from data.uiprototype.objects import Context

class TextBox:
    def __init__(self, size: tuple[int], **options):
        """
        ctx: Context
        size: tuple (x, y, width)
        style:
            bg_color: (50, 50, 50)
            bg_hover: (100, 100, 100)
            bg_active: (75, 75, 75)
            bg_disabled: (25, 25, 25)
            color: (255, 255, 255)
        options:
            disabled: False
            character_limit: 20
            numeric_only: False
            default: ""
        """
        
        # Styling
        self.bg_color: tuple[int] = options.get("bg_color", (25, 25, 25))
        self.bg_hover: tuple[int] = options.get("bg_hover", (100, 100, 100))
        self.bg_selected: tuple[int] = options.get("bg_active", (75, 75, 75))
        self.bg_disabled: tuple[int] = options.get("bg_disabled", (50, 50, 50))
        self.text_color: tuple[int] = options.get("color", (255, 255, 255))

        # Options
        self.disabled: bool = options.get("disabled", False)
        self.char_limit: int = options.get("character_limit", 20)
        self.numeric_only: bool = options.get("numeric_only", False)
        self._value: str = options.get("default", "")[:self.char_limit]

        self.size = size

        self.selected = False
    
    def draw(self, ctx):
        text = ctx.font.render(self._value, True, self.text_color)
        self.rect = text.get_rect()
        self.rect.x = self.size[0]
        self.rect.y = self.size[1]
        self.rect.width = self.size[2]
        
        box = pygame.Rect(
            self.rect.x - 10, self.rect.y - 5,
            self.rect.width + 20, self.rect.height + 10
        )

        if self.selected:
            background = self.bg_selected
        elif self.disabled:
            background = self.bg_disabled
        else:
            background = self.bg_color
            mouse_pos = pygame.mouse.get_pos()
            if box.collidepoint(mouse_pos):
                background = self.bg_hover
        
        pygame.draw.rect(ctx.screen, background, box)
        ctx.screen.blit(text, self.rect)


    def handler(self, event):
        if self.disabled:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.selected = True
            else:
                self.selected = False
        if event.type == pygame.KEYDOWN:
            if not self.selected:
                return
            if event.unicode:
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    self.selected = False
                elif event.key == pygame.K_BACKSPACE:
                    self._value = self._value[:-1]
                elif event.key in (pygame.K_END, pygame.K_DELETE, pygame.K_HOME):
                    return
                elif event.unicode.isascii() and event.unicode not in (",", ";"):
                    self._value += event.unicode
                    self._value = self._value[:self.char_limit]

    @property
    def value(self):
        if self.numeric_only:
            return int(self._value)
        else:
            return self._value