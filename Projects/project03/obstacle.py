import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,panel,x,midY,top):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pipe.png")
        self.rect = self.image.get_rect()
        self.w = self.rect.width
        self.h = self.rect.height
        self.screen = panel
        self.x = x
        self.top = top
        self.setMidY(midY)

        
        #Flip Sprite if Top
        if(top):
            self.image = pygame.transform.rotate(self.image,180)
        self.updateDisplay()

    def updateDisplay(self):
        self.screen.blit(self.image,(self.x,self.y))
        self.rect.x,self.rect.y = self.x,self.y
        
    def step(self):
        self.x -= 3

        self.updateDisplay()

    def setMidY(self,midY):
        diff = 96
        self.midY = midY
        self.y = midY + diff
        if(self.top):
            self.y = midY - diff - self.h
