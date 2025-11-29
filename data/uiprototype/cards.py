
from data.uiprototype.objects import *


vlm = pygame.font.SysFont("Arial", 22)

class CardSprite(pygame.sprite.Sprite):
    def __init__(self, img:str):
        self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_width()//2, self.image.get_height()//2))
        self.rect = self.image.get_rect()
        super().__init__()

    def move(self, pos):
        self.rect.center = pos

class Card():
    def __init__(self, name, hp, dmg, img):
        self.card:CardSprite = CardSprite(img)
        self.pos = (0,0)
        self.name = vlm.render(str(name), True, (255,0,0))
        self.hp = vlm.render(str(hp), True, (255,0,0))
        self.dmg = vlm.render(str(dmg), True, (255,0,0))
    
    def move(self, pos):
        self.pos = pos
        self.card.move(pos)

    def render(self, screen:pygame.Surface):
        screen.blit(self.name, (self.pos[0]-20, self.pos[1]-115))
        screen.blit(self.hp, (self.pos[0]+50, self.pos[1]+95))
        screen.blit(self.dmg, (self.pos[0]-70, self.pos[1]+95))


class CardStats():
    def __init__(self, strength:int, health:int, name:str,elemental:str):
        self.strength = strength
        self.health = health
        self.elemental = elemental
        self.name = name
        self.height = 200
        self.width = 140
        self.kartyafont = pygame.font.SysFont("arial", 22)
    
    def imgload(elemental:str):
        if elemental == "Fire":
            img = pygame.image.load("data/uiprototype/img/fire.png").convert_alpha()
            imgh = img.get_height() // 2
            imgw = img.get_width() // 2
            return pygame.transform.smoothscale(img,(imgw,imgh))
        elif elemental == "Air":
            img = pygame.image.load("data/uiprototype/img/air.png").convert_alpha()
            imgh = img.get_height() // 2
            imgw = img.get_width() // 2
            return pygame.transform.smoothscale(img,(imgw,imgh))
        elif elemental == "Earth":
            img = pygame.image.load("data/uiprototype/img/earth.jpg").convert_alpha()
            imgh = img.get_height() // 2
            imgw = img.get_width() // 2
            return pygame.transform.smoothscale(img,(imgw,imgh))
        else:
            img = pygame.image.load("data/uiprototype/img/water.png").convert_alpha()
            imgh = img.get_height() // 2
            imgw = img.get_width() // 2
            return pygame.transform.smoothscale(img,(imgw,imgh))


class CreateCard(CardStats):
    def __init__(self, strength, health, name, elemental:str):  
        self.elemental = elemental
        self.img = CardStats.imgload(self.elemental)
        self.rect = self.img.get_rect()
        super().__init__(strength, health, name, elemental)

    def location(self, screen, x, y):
        self.rect.topleft = (x,y)
        dmg_text = self.kartyafont.render(str(self.strength), True, (255,0,0))
        hp_text = self.kartyafont.render(str(self.health), True, (255,0,0))
        name_text = self.kartyafont.render(str(self.name), True, (255,0,0))
        #Image
        screen.blit(self.img, self.rect)
        #Name
        screen.blit(name_text, (self.rect.centerx - name_text.get_width() // 2, self.rect.top + 20))
        # Damage
        if self.strength >= 100:
            screen.blit(dmg_text, (self.rect.left + 15, self.rect.bottom - dmg_text.get_height()- 15))
        elif 100 >self.strength > 9:
            screen.blit(dmg_text, (self.rect.left + 19, self.rect.bottom - dmg_text.get_height()- 14))
        else:
            screen.blit(dmg_text, (self.rect.left + 25, self.rect.bottom - dmg_text.get_height()- 14))
        #Health    
        if self.health >= 100:
            screen.blit(hp_text, (self.rect.right - 47, self.rect.bottom - hp_text.get_height()- 15))
        elif 100 > self.health > 9:
             screen.blit(hp_text, (self.rect.right - 44, self.rect.bottom - hp_text.get_height()- 14))
        else:
            screen.blit(hp_text, (self.rect.right - 37, self.rect.bottom - hp_text.get_height()- 14))