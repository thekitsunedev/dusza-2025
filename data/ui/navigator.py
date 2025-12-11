from data.ui.objects import *
from data.ui.cards import *
from data.prototypes.connector import Connector
import pygame_menu
import pygame
import sys
from string import digits, ascii_letters

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
            if self.state == "QUIT": 
                sys.exit(0)
                return
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
        bg = ctx.bg
        ctx.screen.fill(bg)
        msg = ""
        def fight():
            nav.navigate("CardSelection")
        def collection():
            nav.navigate("Collection")
        def dungeon():
            nav.navigate("Dungeons")
        def quit():
            if ctx.save_name != "":
                ctx.conn.createSave(ctx.save_name)
            nav.navigate("QUIT")
        def cards():
            nav.navigate("AllCards")
        def diffChange(value):
            ctx.conn.controller.world.difficulty = int(value)
        
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
        menu.add.range_slider(
            title="Nehézség",
            default=ctx.conn.controller.world.difficulty,
            onchange=diffChange,
            increment=1.0,
            range_values=(0.0, 10.0),
            value_format=lambda x: f"{x:.0f}"            
        )
        menu.add.button("Kilépés", quit)
        
        if ctx.save_name != "":
            ctx.conn.createSave(ctx.save_name)
        
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
        bg = ctx.bg
        cards:dict = ctx.conn.fetchCards("collection")
        x = 10
        y = 10
        ctx.screen.fill(bg)
        for i in cards:
            a = cards[i]
            CreateCard(a["damage"], a["health"],i,a["element"], x, y).location(ctx.screen)
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
        bg = ctx.bg

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
        menu.add.button("Betöltés", saveselection)
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
        self.selected_world = ""


    def run(self, ctx:Context, nav:Navigator):
        bg = ctx.bg
        ctx.save_name = ""
        
        worlds:list[str] = ctx.conn.fetchWorlds() 

        def back():
            nav.navigate("Starter")

        def loadWorld():
            ctx.conn.loadWorld(self.selected_world)
            nav.navigate("MainMenu")
        
        def onSaveChange(value):
            ctx.save_name = value


        menu = pygame_menu.Menu(
        title="Új játék",
        width=1920,
        height=1080,
        theme=pygame_menu.themes.THEME_DARK
        )

        menu.add.dropselect(
            title="Világ",
            items=[(world, i) for i, world in enumerate(worlds)],
            default=0,
            onchange=self.selectWorld,
            placeholder="Válassz világot"
        )
        menu.add.text_input(
            title="Mentés név: ",
            default="",
            maxchar=20,
            onchange=onSaveChange,
            valid_chars=list(ascii_letters) + list(digits) + [" ", "_", "-", "'"]
        )
        menu.add.button("Betöltés", loadWorld)
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
    
    def selectWorld(self, value, index):
        self.selected_world = value[0][0]


class AllCards(Scene):
    def __init__(self, name):
        super().__init__(name)
    def run(self, ctx:Context, nav:Navigator):
        bg = ctx.bg
        cards:dict = ctx.conn.fetchCards("cards")
        x = 10
        y = 10
        o = 0
        ctx.screen.fill(bg)
        Button((255,0,0),200,900,200,50,"Vissza").draw(ctx.screen)
        for i in cards:
            a = cards[i]
            if o < 9:
                CreateCard(a["damage"], a["health"],i,a["element"], x, y).location(ctx.screen)
                if o == 9:
                    y = 50
                    x = 50
            else:
                CreateCard(a["damage"], a["health"],i,a["element"], x, y+100).location(ctx.screen)
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
        bg = ctx.bg
        dungeons: dict = ctx.conn.fetchDungeons()
        x = 400
        y = 300
        ctx.screen.fill(bg)
        for i in dungeons:
            a = dungeons[i]
            CreateKazamata(i,a["reward"],a["type"]).draw(ctx.screen,x,y)
            x += 370
        
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
        self.dungeon = ""
    
    def run(self, ctx:Context, nav:Navigator):
        bg = (127,127,127)

        def startFight(value, index):
            ctx.dungeon_name = value[0][1]
            nav.navigate("Fight")

        men = pygame_menu.Menu(
            title="Világ választás",
            width=1920,
            height=1080,
            theme=pygame_menu.themes.THEME_DARK
        )


        dungeons = ctx.conn.fetchDungeons()
        items = []
        for dungeon in dungeons:
            dun = dungeons[dungeon]
            text = f"{dungeon} {dun['type']} {dun['reward']}"
            items.append((text, dungeon)),

        men.add.dropselect(
            title="Kazamata",
            items=items,
            onchange=startFight,
            selection_box_width=700
        )

        nav.running = True
        while nav.running:
            ctx.screen.fill(bg)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    nav.navigate("QUIT")
                    return
            men.update(events)
            men.draw(ctx.screen)
            pygame.display.update()
    

class Fight(Scene):
    def __init__(self, name):
        super().__init__(name)
    def run(self, ctx:Context, nav:Navigator):
        bg = ctx.bg
        ctx.screen.fill(bg)
        status = ctx.conn.prepareFight(ctx.dungeon_name)
        clock = pygame.time.Clock()
        timeout = 61

        def draw(status):
            active_card_name = status["active_card"].get("name", "")
            active_enemy_name = status["active_enemy"].get("name", "")     

            # Draw player's cards
            x = 100
            y = 700
            for card_name in status["deck"]:
                card = status["deck"][card_name]
                offset = 0
                if card_name == active_card_name:
                    offset = -160
                elif card["health"] == 0:
                    offset = 100
                CreateCard(card["damage"], card["health"],card_name,card["element"],x,y + offset).location(ctx.screen)
                x += 200


            # Draw enemy's cards
            y = 70
            x = 100
            for card_name in status["enemy_deck"]:
                card = status["enemy_deck"][card_name]
                offset = 0
                if card_name == active_enemy_name:
                    offset = 160
                elif card["health"] == 0:
                    offset = -100
                CreateCard(card["damage"], card["health"],card_name,card["element"],x,y+offset).location(ctx.screen)
                x += 200

            # Draw text
            enemy_title = ctx.font2.render("Ellenfél kártyái",
                    True, "black")
            enemy_box = enemy_title.get_rect()
            enemy_box.x = 10
            enemy_box.y = 10
            enemy_rect = pygame.draw.rect(ctx.screen, ctx.bg, 
                (enemy_box.x, enemy_box.y, enemy_box.width, enemy_box.height))
            ctx.screen.blit(enemy_title, enemy_rect)

            player_title = ctx.font2.render("Játékos kártyái",
                    True, "black")
            player_box = player_title.get_rect()
            player_box.x = 10
            player_box.y = 1030
            player_rect = pygame.draw.rect(ctx.screen, ctx.bg, 
                (player_box.x, player_box.y, player_box.width, player_box.height))
            ctx.screen.blit(player_title, player_rect)


        draw(status)

        def draw_result(status):
            ctx.screen.fill("#2f2f2f")
            result = status["result"]
            match(result["status"]):
                case "jatekos vesztett":
                    text = ctx.font.render("Játékos Vesztett", True, "white")
                    text_box = text.get_rect()
                    text_box.x = 1920//2 - text_box.width // 2
                    text_box.y = 1080//2 - text_box.height // 2
                    rect = pygame.draw.rect(ctx.screen, "#2f2f2f",
                        (text_box.x, text_box.y, text_box.width, text_box.height))
                    ctx.screen.blit(text, rect)
                case "jatekos nyert":
                    text = ctx.font.render("Játékos Nyert", True, "white")
                    text_box = text.get_rect()
                    text_box.x = 1920//2 - text_box.width // 2
                    text_box.y = 1080//2 - text_box.height // 2
                    rect = pygame.draw.rect(ctx.screen, "#2f2f2f",
                        (text_box.x, text_box.y, text_box.width, text_box.height))
                    ctx.screen.blit(text, rect)

                    reward = result["reward"].get("stat", "kartya")
                    if reward == "kartya":
                        text = ctx.font2.render(f"Nyeremény: Kártya {result["reward"]["name"]}", True, "white")
                        text_box = text.get_rect()
                        text_box.x = 1920//2 - text_box.width // 2
                        text_box.y = 1080//2 - text_box.height // 2 + 100
                        rect = pygame.draw.rect(ctx.screen, "#2f2f2f",
                            (text_box.x, text_box.y, text_box.width, text_box.height))
                        ctx.screen.blit(text, rect)
                    elif reward == "eletero":
                        text = ctx.font2.render(f"Nyeremény: +2 Életerő {result["reward"]["card"]}", True, "white")
                        text_box = text.get_rect()
                        text_box.x = 1920//2 - text_box.width // 2
                        text_box.y = 1080//2 - text_box.height // 2 + 100
                        rect = pygame.draw.rect(ctx.screen, "#2f2f2f",
                            (text_box.x, text_box.y, text_box.width, text_box.height))
                        ctx.screen.blit(text, rect)
                    elif reward == "sebzes":
                        text = ctx.font2.render(f"Nyeremény: +1 Sebzés {result["reward"]["card"]}", True, "white")
                        text_box = text.get_rect()
                        text_box.x = 1920//2 - text_box.width // 2
                        text_box.y = 1080//2 - text_box.height // 2 + 100
                        rect = pygame.draw.rect(ctx.screen, "#2f2f2f",
                            (text_box.x, text_box.y, text_box.width, text_box.height))
                        ctx.screen.blit(text, rect)
            
        
            


        iters = []
        for st in ctx.conn.iterateFight():
            iters.append(st)

        timer = 0
        while nav.running:

            ctx.screen.fill("#7f7f7f")        
            events = pygame.event.get()
            if "result" not in status.keys():
                draw(status)
            else:
                draw_result(status)
            timer = (timer + 1) % timeout
            if timer == timeout - 1:
                if len(iters) > 0:
                    status = iters.pop(0)
                elif timeout != 601:
                    timeout = 601
                    timer = 0
                else:
                    nav.navigate("MainMenu")
                    return


            for event in events:
                if event.type == pygame.QUIT:
                    nav.navigate("QUIT")
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if timeout == 601:
                        nav.navigate("MainMenu")
                        return
                    timer = timeout - 2
            pygame.display.update()
            clock.tick(60)


class CardSelection(Scene):
    def __init__(self, name):
        super().__init__(name)
    def run(self, ctx:Context, nav:Navigator):
        bg = ctx.bg
        ctx.screen.fill(bg)
        cards:dict = ctx.conn.fetchCards("collection")
        x = 50
        y = 50
        y_count = 0
        deck = []
        onscreen = []
        for i in cards:
            a = cards[i]
            card = CreateCard(a["damage"], a["health"],i,a["element"],x,y)
            card.location(ctx.screen)
            onscreen.append(card)
            x += 190
            y_count = (y_count + 1) % 10
            if y_count == 9:
                y += 280
                x = 50

        while nav.running:
            events = pygame.event.get()
            ctx.screen.fill(bg)
            Button((255,0,0),200,900,200,50,"Harc").draw(ctx.screen)
            for card in onscreen:
                card.location(ctx.screen)

            for event in events:
                if event.type == pygame.QUIT:
                    nav.navigate("QUIT")
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if  Button((255,0,0),200,900,200,50,"Vissza").isOver(pygame.mouse.get_pos()):
                        ctx.conn.createDeck(deck)
                        nav.navigate("DungeonSelection")
                for i in onscreen:
                    if i.click(event):
                        if len(deck) >= ctx.conn.deck_limit:
                            i.selected = False
                        if i.selected:
                            deck.append(i.name)
                        else:
                            if i.name in deck:
                                deck.remove(i.name)



            pygame.display.update()