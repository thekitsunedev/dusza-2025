
from data.uiprototype.objects import *


vlm = pygame.font.SysFont("Arial", 22)

class CardSprite(pygame.sprite.Sprite):
    def __init__(self, img:str):
        super().__init__()

        self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_width()//2, self.image.get_height()//2))

        self.rect = self.image.get_rect()

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