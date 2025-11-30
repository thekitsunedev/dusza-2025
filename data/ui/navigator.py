from data.ui.objects import *
from data.ui.cards import *
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
            nav.navigate("CardSelection")
        def collection():
            nav.navigate("Collection")
        def dungeon():
            nav.navigate("Dungeons")
        def quit():
            nav.navigate("QUIT")
        def cards():
            nav.navigate("AllCards")

        
        menu = pygame_menu.Menu(
            title="",
            width=1920,
            height=1080,
            theme=pygame_menu.themes.THEME_DARK,

        )

        menu.add.button("Harc", fight)
        menu.add.button("Kazamaták", dungeon)
        menu.add.button("Gyűjtemény", collection)
        menu.add.button("Kártyák", cards)
        menu.add.button("Kilépés", quit)
        
        
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
        cards:dict = ctx.conn.fetchCards("collection")
        x = 10
        y = 10
        ctx.screen.fill(bg)
        for i in cards:
            a = cards[i]
            CreateCard(a["damage"], a["health"],i,a["element"]).location(ctx.screen, x, y)
            x += 190
        
        while nav.running:
            events = pygame.event.get()
            
            vissza = Button((255,0,0),200,900,200,50,"Vissza").draw(ctx.screen)

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if  Button((255,0,0),200,900,200,50,"Vissza").isOver(pygame.mouse.get_pos()):
                        nav.navigate("MainMenu")

                if event.type == pygame.QUIT:
                    nav.navigate("QUIT")
                    return
            pygame.display.update()
        

class StarterMenu(Scene):
    def __init__(self, name):
        super().__init__(name)
    def run(self, ctx:Context, nav:Navigator):
        bg = (127,127,127)

        def worldselection():
            nav.navigate("WorldSelect")

        def saveselection():
            nav.navigate("SaveSelect")
        
        def editor():
            nav.navigate("WorldEditor")
        
        def quit():
            nav.navigate("QUIT")
        
        menu = pygame_menu.Menu(
            title="",
            width=1920,
            height=1080,
            theme=pygame_menu.themes.THEME_DARK,

        )

        menu.add.button("Új játék", worldselection)
        menu.add.button("Betőltés", saveselection)
        menu.add.button("Világ szerkesztő", editor)
        menu.add.button("Kilépés", quit)
        
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


class WorldSelect(Scene):
    def __init__(self, name):
        super().__init__(name)
    def run(self, ctx:Context, nav:Navigator):
        bg = (127,127,127)
        
        worlds:list[str] = ctx.conn.fetchWorlds() 

        def back():
            nav.navigate("Starter")

        def button(world):
            ctx.conn.loadWorld(world)
            nav.navigate("MainMenu")

        menu = pygame_menu.Menu(
        title="Világ választás",
        width=1920,
        height=1080,
        theme=pygame_menu.themes.THEME_DARK,

        )

        for i in worlds:
            menu.add.button(i, lambda:button(i))

        menu.add.button("Kilépés", back)
        
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


class AllCards(Scene):
    def __init__(self, name):
        super().__init__(name)
    def run(self, ctx:Context, nav:Navigator):
        bg = (127,127,127)
        cards:dict = ctx.conn.fetchCards("cards")
        x = 10
        y = 10
        ctx.screen.fill(bg)
        Button((255,0,0),200,900,200,50,"Vissza").draw(ctx.screen)
        for i in cards:
            a = cards[i]
            CreateCard(a["damage"], a["health"],i,a["element"]).location(ctx.screen, x, y)
            x += 190
    
        while nav.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    nav.navigate("QUIT")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if  Button((255,0,0),200,900,200,50,"Vissza").isOver(pygame.mouse.get_pos()):
                        nav.navigate("MainMenu")
                    return
            pygame.display.update()


class Dungeons(Scene):
    def __init__(self, name):
        super().__init__(name)
    def run(self, ctx:Context, nav:Navigator):
        bg = (127,127,127)
        cards:dict = ctx.conn.fetchCards("cards")
        x = 10
        y = 10
        ctx.screen.fill(bg)
        Button((255,0,0),200,900,200,50,"Vissza").draw(ctx.screen)
        while nav.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    nav.navigate("QUIT")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if  Button((255,0,0),200,900,200,50,"Vissza").isOver(pygame.mouse.get_pos()):
                        nav.navigate("MainMenu")
                    return
            pygame.display.update()


class DungeonSelection(Scene):
    def __init__(self, name):
        super().__init__(name)
    def run(self, ctx:Context, nav:Navigator):
        bg = (127,127,127)

        def action(name):
            ctx.conn.prepareFight(name)



        menu = pygame_menu.Menu(
            title="",
            width=1920,
            height=1080,
            theme=pygame_menu.themes.THEME_DARK,

        )

        dungeons: dict = ctx.conn.fetchDungeons()

        for i in dungeons:
            menu.add.button(i, lambda:action(i))



        while nav.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    nav.navigate("QUIT")
                    return
            pygame.display.update()
    

class Fight(Scene):
    def __init__(self, name):
        super().__init__(name)
    def run(self, ctx:Context, nav:Navigator):
        bg = (127,127,127)
        ctx.screen.fill(bg)
        while nav.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    nav.navigate("QUIT")
                    return
            pygame.display.update()




class CardSelection(Scene):
    def __init__(self, name):
        super().__init__(name)
    def run(self, ctx:Context, nav:Navigator):
        bg = (127,127,127)
        ctx.screen.fill(bg)
        cards:dict = ctx.conn.fetchCards("collection")
        x = 50
        y = 50
        onscreen = []
        for i in cards:
            a = cards[i]
            card = CreateCard(a["damage"], a["health"],i,a["element"],x,y)
            card.location(ctx.screen)
            onscreen.append(card)
            x += 190

        while nav.running:
            events = pygame.event.get()
            ctx.screen.fill(bg)
            for card in onscreen:
                card.location(ctx.screen)

            for event in events:
                if event.type == pygame.QUIT:
                    nav.navigate("QUIT")
                    return
                for i in onscreen:
                    if i.click(event):
                        print(f"{i.name}")


            pygame.display.update()