import pygame

class Cards():
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
            return pygame.image.load("data/uiprototype/img/fire.png").convert_alpha()
        elif elemental == "Air":
            return pygame.image.load("data/uiprototype/img/Air.png").convert_alpha()
        elif elemental == "Earth":
            return pygame.image.load("data/uiprototype/img/earth.jpg").convert_alpha()
        else:
            return pygame.image.load("data/uiprototype/img/water.png").convert_alpha()

        



class CreateCard(Cards):
    def __init__(self, strength, health, name, elemental:str):  
        self.elemental = elemental
        self.img = Cards.imgload(self.elemental)
        self.imgh = self.img.get_height() // 2
        self.imgw = self.img.get_width() // 2
        self.img = pygame.transform.smoothscale(self.img, (self.imgw, self.imgh))
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
