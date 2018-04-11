import neat
import sys
import random
import pickle
from gvGame import Game


GENERATION = 0
MAX_FITNESS = 0
BEST_GENOME = 0

def eval_genomes(genomes, config):
    i = 0
    global SCORE
    global GENERATION, MAX_FITNESS, BEST_GENOME

    GENERATION += 1
    game = Game()
    for genome_id, genome in genomes:
        
        genome.fitness = game.game(genome, config, 1)
        print("")
        print("Generation: " + str(GENERATION) + ", Genome: " + str(i) + ", My Fitness: " + str(round(genome.fitness)) + ", Best Fitness: " + str(round(MAX_FITNESS)))
        if genome.fitness >= MAX_FITNESS:
            MAX_FITNESS = genome.fitness
            BEST_GENOME = genome
        SCORE = 0
        i+=1

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config')

pop = neat.Population(config)
stats = neat.StatisticsReporter()
pop.add_reporter(stats)

winner = pop.run(eval_genomes, 80)

print(winner)

outputDir = 'bestGenomes'
outputFile = open(outputDir+'\_'+str(int(MAX_FITNESS))+'.p','wb' )
pickle.dump(winner, outputFile)
outputFile.close();

sys.exit();
