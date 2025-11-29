from data.uiprototype.objects import *
from data.uiprototype.cards import *
from data.prototypes.connector import Connector
import pygame_menu

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
        def fight():
            print("Harc")
        def collection():
            nav.navigate("Collection")
        def quit():
            nav.navigate("QUIT")
        
        menu = pygame_menu.Menu(
            title="",
            width=1920,
            height=1080,
            theme=pygame_menu.themes.THEME_DARK,

        )

        menu.add.button("Harc", fight)
        menu.add.button("Gyűjtemény", collection)
        menu.add.button("Kilépés",quit)
        
        
        while nav.running:
            ctx.screen.fill(bg)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    nav.navigate("QUIT")
                    return
            if menu.is_enabled():
                menu.update(events)
                menu.draw(ctx.screen)
            pygame.display.update()
                

            #update
            pygame.display.update()

            
class CollectionScene(Scene):
    def __init__(self, name):
        super().__init__(name)
    def run(self, ctx:Context, nav:Navigator):
        bg = (127,127,127)
        
        lista2 = ["Monkey","Holló","IDK","TAKONY"]
        a = 0
        n = 0
        hp = 10
        dmg = 10
        x = 50

        ctx.screen.fill(bg)
        for i in lista2:
            if n < 9:
                i = CreateCard(dmg,hp,lista2[a],"Fire").location(ctx.screen,x,0)
                
            elif n < 18:
                if n == 9: x = 50
                i = CreateCard(dmg,hp,lista2[a],"Air").location(ctx.screen,x,280)
            elif n < 27:
                if n == 18: x = 50
                i = CreateCard(dmg,hp,lista2[a],"Earth").location(ctx.screen,x,560)
            else:
                if n == 27: x = 50
                i = CreateCard(dmg,hp,lista2[a],"Tűz").location(ctx.screen,x,840)
            x += 200
            if a == len(lista2)-1:break
            a += 1
            n += 1

        
        while nav.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    nav.navigate("QUIT")
                    return
            pygame.display.update()
        
            
class StarterMenu(Scene):
    def __init__(self, name):
        super().__init__(name)
    def run(self, ctx:Context, nav:Navigator):
        bg = (127,127,127)

        def mainmenu():
            nav.navigate("MainMenu")

        def editor():
            nav.navigate("WorldEditor")
        
        menu = pygame_menu.Menu(
            title="",
            width=1920,
            height=1080,
            theme=pygame_menu.themes.THEME_DARK,

        )

        menu.add.button("Új játék", mainmenu)
        menu.add.button("Editor", editor)
        
        while nav.running:
            ctx.screen.fill(bg)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    nav.navigate("QUIT")
                    return
            if menu.is_enabled():
                menu.update(events)
                menu.draw(ctx.screen)
            pygame.display.update()