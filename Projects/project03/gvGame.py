#Inspiration/Learning From:
#https://github.com/llSourcell/neuroevolution-for-flappy-birds

import pygame
from pygame.locals import *
import sys
import random
from player import Player
from obstacle import Obstacle
import neat
import pickle

class Game():
    def game(self, genome, config, mode):
        #Set Mode (0 = Play, 1 = Train)
        self.mode = mode
        
        FPS = 60
        if(self.mode==1):
            FPS = 200
        WIDTH = 288
        HEIGHT = 512
        running = True
        paused = False
        BACKGROUND = pygame.image.load("bg.png")        
        
        
        #NEAT Stuff
        if(self.mode==1):
            fitness = 0;
            ffnet = neat.nn.FeedForwardNetwork.create(genome,config)
        
        pygame.init()
        CLOCK = pygame.time.Clock()
        PANEL = pygame.display.set_mode((WIDTH,HEIGHT))
        score = 0
        time = 0
        
        #Player Character
        player = Player(PANEL)
        
        #Obstacles
        obsU1 = Obstacle(PANEL,512,256,False)
        obsL1 = Obstacle(PANEL,512,256,True)
        obsU2 = Obstacle(PANEL,512+200,160,False)
        obsL2 = Obstacle(PANEL,512+200,160,True)
        
        
        #Create List of Obstacles for easy handling
        obsList = []
        obsList.append(obsU1)
        obsList.append(obsL1)
        obsList.append(obsU2)
        obsList.append(obsL2)
        
        #Create Group of Sprites for Collision Detection
        obsGroup = pygame.sprite.Group()
        myNum = 0
        for obs in obsList:
            obsGroup.add(obs)
            #Let's also use this time to set the initial midY
            if(myNum==0 or myNum==2):
                myMid = random.randint(160,512-160)
            obs.setMidY(myMid)
            myNum+=1

        #Game Loop
        while running:
            time+=1
            if(self.mode==1 and not paused):
                #Get Closest Obs
                minBotX = 1000
                minTopX = 1000
                botObs = None
                topObs = None
                for obs in obsList:
                    if(obs.top and obs.x<minTopX):
                        topObs = obs
                    if(not obs.top and obs.x<minBotX):
                        botObs = obs
                closestMid = topObs.midY
                input = (player.y,topObs.x,topObs.y,botObs.y)
                #distanceToMid = abs(player.y - closestMid)
                distanceToMid = (((player.y - closestMid)**2)*100)/(512*512)
                #fitness = time + score - distanceToMid
                fitness = score - distanceToMid + (time/10.0)
                output = ffnet.activate(input)
                if(output[0]>=0.5):
                   player.jump()

            #Get Inputs
            for event in pygame.event.get():
                if(event.type == KEYDOWN):
                    #Player Jump
                    if(event.key == K_SPACE and mode==0):
                        player.jump()
                    if(event.key == K_TAB and mode==0):
                        paused = not paused
                    #Close Game With Escape Key
                    if(event.key == K_ESCAPE):
                        self.close()
            if(not paused):
                PANEL.blit(BACKGROUND,(0,0))
                player.step()
                myMid = random.randint(160,512-160)
                for obs in obsList:
                    obs.step()
                    #Reset Obs
                    if(obs.x < 0 - obs.w):
                        obs.x = obs.x + WIDTH * 1.5
                        obs.setMidY(myMid)
                        score+=5
                #Check Collision
                collision = pygame.sprite.spritecollideany(player,obsGroup)

                #Game Over Conditions
                if(collision!=None or player.y<=0 or player.y>=HEIGHT):
                    if(self.mode==0):
                        print("GAME OVER")
                        self.close()
                    if(self.mode==1):
                        return fitness
                
            
            pygame.display.update()
            CLOCK.tick(FPS)    

    def close(self):
        pygame.display.quit()
        pygame.quit()
        sys.exit()

