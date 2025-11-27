from data.uiprototype.objects import *
from data.uiprototype.cards import *

class Scene:
    def __init__(self, name:str):
        self.name = name
    
    def run(self): pass


class Navigator():
    def __init__(self, ctx:Context, scenes:dict[str:Scene]):
        self.ctx = ctx
        self.scenes:dict[str:Scene] = scenes
        self.running = True
        self.state = ""
        
    def start(self, name:str):
        self.state = name
        while True:
            if self.state == "QUIT": return
            self.running = True
            self.scenes[self.state].run(self.ctx, self)

    def navigate(self, name:str)-> None:
        self.state = name
        self.running = False 



class MenuScene(Scene):
    def __init__(self, name):
        super().__init__(name)

    def run(self, ctx:Context, nav:Navigator):
        text = ctx.font.render("Gyűjtemény", True, (255,255,255))
        rect = text.get_rect(topleft=(100,10))
        bg = (127,127,127)
        ctx.screen.fill(bg)
        msg = ""
        while nav.running:
            #setup
            events = pygame.event.get()

            # rajz
            ctx.screen.fill(bg)

            menu_items = ["Harc", "Gyűjtemény", "Kazamaták", "Beállítások", "Világ szerkesztő", "Kilépés"]
            buttons = []

            y_start = 100
            vertical_spacing = 150
            mouse_pos = pygame.mouse.get_pos()

            for i, text_str in enumerate(menu_items):

                
                text_color = (255, 255, 255)
                bg_color = (50, 50, 50)       
            
                
                text = ctx.font.render(text_str, True, text_color)
                rect = text.get_rect()
                rect.centerx = ctx.screen.get_width() // 2
                rect.y = y_start + i * vertical_spacing

                
                box_rect = pygame.Rect(
                    rect.x - 10, rect.y - 5,
                    rect.width + 20, rect.height + 10
                )

                # Hover effekt
                if box_rect.collidepoint(mouse_pos):
                    text_color = (200, 200, 200)     
                    bg_color = (100, 100, 100)       
                    border_color = (200, 200, 200)   
                    text = ctx.font.render(text_str, True, text_color)

                # rajzolás
                pygame.draw.rect(ctx.screen, bg_color, box_rect)         
                pygame.draw.rect(ctx.screen, bg, box_rect, 2)  
                ctx.screen.blit(text, rect)                              

                buttons.append((box_rect, text_str))


            #event
            if events:
                for event in events:
                    if event.type == pygame.QUIT:
                        nav.navigate("QUIT")
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if rect.collidepoint(event.pos):
                            ## DEBUG
                            nav.navigate("WorldEditor")
                            #nav.navigate("Collection")
                            return
                

            #update
            pygame.display.update()

            
class CollectionScene(Scene):
    def __init__(self, name):
        super().__init__(name)
    def run(self, ctx:Context, nav:Navigator):
        text = ctx.font.render("Monkey", True, (255,255,255))
        rect = text.get_rect(topleft=(300,10))
        bg = (127,127,127)
        ctx.screen.fill(bg)
        while nav.running:
            pygame.display.update()
            events = pygame.event.get()
            ctx.screen.blit(text,rect)
            pygame.draw.rect(ctx.screen,(255,0,0), rect, 2)

            for event in events:
                if event.type == pygame.QUIT:
                    nav.navigate("QUIT")
                    return
        
            



    
        