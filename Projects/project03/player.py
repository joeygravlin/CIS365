import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,panel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("logo.png")
        self.x = 48
        self.y = 256
        self.rect = self.image.get_rect()
        self.h = self.rect.height
        self.screen = panel
        self.jumpHeight = 12
        self.ysp = 0
        self.yspMax = 10
        self.grav = 1
        #self.jumping = False
        self.updateDisplay(self.x,self.y)

    def updateDisplay(self,x,y):
        self.screen.blit(self.image,(x,y))
        self.rect.x, self.rect.y = x,y

    def step(self):
        if(self.ysp>self.yspMax):
            self.ysp = self.yspMax
        self.y += self.ysp
        self.ysp += self.grav
        self.updateDisplay(self.x,self.y)

    def jump(self):
        self.ysp = -self.jumpHeight
        #self.jumping = True
