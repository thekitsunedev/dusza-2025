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
            text = ctx.font.render("Gyűjtemény", True, (255,255,255))
            rect = text.get_rect(topleft=(100,10))
            ctx.screen.blit(text, rect)
            pygame.draw.rect(ctx.screen,(255,0,0), rect, 2)

            #event
            if events:
                for event in events:
                    if event.type == pygame.QUIT:
                        nav.navigate("QUIT")
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if rect.collidepoint(event.pos):
                            print("fasz")
                            nav.navigate("Collection")
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
            



    
        