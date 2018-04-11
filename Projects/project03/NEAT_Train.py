import neat
import sys
import random
import pickle
from gvGame import Game
import myGlobals

#Variables
GENERATION = 0
MAX_FITNESS = 0
BEST_GENOME = 0
myGlobals.SCORE = 0
highScore = 0
#Population Run Function:
#Plays game and then gets fitness for each genome
def eval_genomes(genomes, config):
    i = 0
    global GENERATION, MAX_FITNESS, BEST_GENOME, highScore

    GENERATION += 1
    #Instantiate game
    game = Game()
    #Iterate through each genome seperately (for now, might change in future)
    for genome_id, genome in genomes:
        #Run game and return fitness
        genome.fitness = game.game(genome, config, 1)
        #Print Results in Console
        print("Gen:" + str(GENERATION) + " Gnm:" + str(i) + " MyFit:" + str(round(genome.fitness)) + " TopFit:" + str(round(MAX_FITNESS)) + " TopSCR:"+str(highScore))
        if genome.fitness >= MAX_FITNESS:
            MAX_FITNESS = genome.fitness
            BEST_GENOME = genome
        if(myGlobals.SCORE > highScore):
            highScore = myGlobals.SCORE
        myGlobals.SCORE = 0
        i+=1

#Load Neat Config
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config')
#Create population
pop = neat.Population(config)
stats = neat.StatisticsReporter()
pop.add_reporter(stats)

#Run all generations and return best genome
bestGenome = pop.run(eval_genomes, 80)

print(bestGenome)

#Save genome via pickle
outputDir = 'bestGenomes'
outputFile = open(outputDir+'\_'+str(int(MAX_FITNESS))+'.p','wb' )
pickle.dump(bestGenome, outputFile)
outputFile.close();

sys.exit();
