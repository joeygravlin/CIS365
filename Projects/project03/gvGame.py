# Inspiration/Learning From:
# https://github.com/llSourcell/neuroevolution-for-flappy-birds

import pygame
from pygame.locals import *
import sys
import random
from player import Player
from obstacle import Obstacle
import neat
import pickle
import myGlobals

myGlobals.init()


class Game():
    def game(self, genome, config, mode):
        # Set Mode (0 = Play, 1 = Train)
        self.mode = mode

        FPS = 60
        if(self.mode == 1):
            FPS = 800
        WIDTH = 288
        HEIGHT = 512
        running = True
        paused = False
        BACKGROUND = pygame.image.load("bg.png")
        # Last Obstacle Jumped Over
        lastObst = None
        # closest mid point
        closestMid = 0
        botObs = None
        topObs = None
        closestX = 0

        lastObst = None
        lastYDiff=0
        lastDist2Mid=0
        bonus=0

        # NEAT Stuff
        if(self.mode == 1):
            fitness = 0
            ffnet = neat.nn.FeedForwardNetwork.create(genome, config)

        pygame.init()
        CLOCK = pygame.time.Clock()
        PANEL = pygame.display.set_mode((WIDTH, HEIGHT))
        time = 0

        # Player Character
        player = Player(PANEL)

        # Obstacles
        obsU1 = Obstacle(PANEL, 300, 256, False)
        obsL1 = Obstacle(PANEL, 300, 256, True)
        obsU2 = Obstacle(PANEL, 300+200, 160, False)
        obsL2 = Obstacle(PANEL, 300+200, 160, True)

        # Create List of Obstacles for easy handling
        obsList = []
        obsList.append(obsU1)
        obsList.append(obsL1)
        obsList.append(obsU2)
        obsList.append(obsL2)

        # Create Group of Sprites for Collision Detection
        obsGroup = pygame.sprite.Group()
        myNum = 0
        for obs in obsList:
            obsGroup.add(obs)
            # Let's also use this time to set the initial midY
            if(myNum == 0 or myNum == 2):
                myMid = self.getNewMid()
            obs.setMidY(myMid)
            myNum += 1

        # Game Loop
        while running:
            time += 1
            if(self.mode == 1 and not paused):
                # Get Closest Obs
                minBotX = 1000
                minTopX = 1000
                botObs = None
                topObs = None
                for obs in obsList:
                    if(obs.top and obs.x < minTopX and obs.x > player.x):
                        topObs = obs
                        minTopX = topObs.x
                    if(not obs.top and obs.x < minBotX and obs.x > player.x):
                        botObs = obs
                        minBotX = botObs.x
                closestMid = topObs.midY
                closestX = topObs.x

                #input = (player.y,topObs.x,closestMid)
                yDiff = abs(player.y - closestMid)
                yDiffTop = abs(player.y - (topObs.y+320))
                yDiffBot = abs(player.y - (botObs.y))
                #distanceToMid = abs(player.y - closestMid)
                distanceToMid = (((player.y - closestMid)**2)+((player.x - closestX)**2))**(1/2)/10

                #FITNESS FUNCTION
                if(yDiff < 25 or (yDiff < lastYDiff and player.y < botObs.y and player.y > topObs.y + 320)):
                    myGlobals.SCORE += 1
                if (yDiff > lastYDiff and (player.y > botObs.y or player.y < topObs.y + 320)):
                    myGlobals.SCORE -= 1
                if(closestX - player.x <= 50 and (distanceToMid <= 5)):
                    myGlobals.SCORE += 1
                    bonus+=1

                #current direction
                lastYDiff = abs(player.y - closestMid)
                lastDist2Mid = distanceToMid

                #NEAT-python inputs
                input = (yDiff, yDiffTop, yDiffBot, closestX)

                #pygame.draw.line(PANEL, (57,255,20), (topObs.x,topObs.y+320), (0,topObs.y+320))
                #pygame.draw.line(PANEL, (57,255,20), (botObs.x,botObs.y), (0,botObs.y))
                # pygame.draw.line(PANEL, (0,0,0), (player.x+34,player.y+18), (player.x+closestX-26,closestMid))
                # pygame.draw.line(PANEL, (0,0,0), (player.x+34,player.y+18), (player.x+closestX-26,topObs.y+320))
                # pygame.draw.line(PANEL, (0,0,0), (player.x+34,player.y+18), (player.x+closestX-26,botObs.y))
                # pygame.display.flip()

                #fitness = time + SCORE - distanceToMid
                fitness = myGlobals.SCORE

                # Get Output
                output = ffnet.activate(input)
                # Jump if output is above threshold
                if(output[0] >= 0.5):
                    player.jump()

            # Get Inputs
            for event in pygame.event.get():
                if(event.type == KEYDOWN):
                    # Player Jump
                    if(event.key == K_SPACE and mode == 0):
                        player.jump()
                    if(event.key == K_TAB and mode == 0):
                        paused = not paused
                    # Close Game With Escape Key
                    if(event.key == K_ESCAPE):
                        self.close()

            if(not paused):
                PANEL.blit(BACKGROUND, (0, 0))
                myfont = pygame.font.SysFont('Arial', 12)
                playerYText = myfont.render(
                    "playerY:  "+str(player.y), False, (0, 0, 0))
                distToMidText = myfont.render(
                    "Distance2Mid:  "+str(distanceToMid), False, (0, 0, 0))
                xMidText = myfont.render(
                    "closestX:  "+str(closestX), False, (0, 0, 0))
                bonusText = myfont.render(
                    "numBonuses:  "+str(bonus), False, (0, 0, 0))
                scoreText = myfont.render(
                    "FITNESS:  "+str(myGlobals.SCORE), False, (0, 0, 0))

                PANEL.blit(playerYText, (20, 20))
                PANEL.blit(distToMidText, (20, 40))
                PANEL.blit(xMidText, (20, 60))
                PANEL.blit(bonusText, (20, 80))
                PANEL.blit(scoreText, (20, 100))
                player.step()
                myMid = self.getNewMid()
                for obs in obsList:
                    obs.step()
                    # Reset Obs
                    if(obs.x < 0 - obs.w):
                        obs.x = obs.x + WIDTH * 1.5
                        obs.setMidY(myMid)
                    # Up Score
                    if(obs.top and obs.x < player.x and lastObst != obs):
                        myGlobals.SCORE += 10
                        lastObst = obs
                        print('SCORE: ' + str(myGlobals.SCORE))
                # Check Collision
                collision = pygame.sprite.spritecollideany(player, obsGroup)

                # Game Over Conditions
                if(collision != None or player.y <= 0 or player.y >= HEIGHT):
                    if(self.mode == 0):
                        print("GAME OVER")
                        self.close()
                    if(self.mode == 1):
                        return fitness

            pygame.display.update()
            CLOCK.tick(FPS)

    def getNewMid(self):
        return random.choice([160, 256, 340])

    def close(self):
        pygame.display.quit()
        pygame.quit()
        sys.exit()
