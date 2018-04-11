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
    print("Generation: " + str(GENERATION) + ", My Fitness: " + str(genome.fitness) + "Best Fitness: " + str(MAX_FITNESS))
    if genome.fitness >= MAX_FITNESS:
            MAX_FITNESS = genome.fitness
            BEST_GENOME = genome
        SCORE = 0
        i+=1

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config')

genomeFile = 'bestGenomes/_955.p'
genome = pickle.load(open(genomeFile,'rb'))

fitnessScores = []
game = Game()
for i in range(10):
    fitness = game.game(genome, config,1)
    SCORE = 0
    print('Fitness is %f'% fitness)
    fitnessScores.append(fitness)

game.close()
sys.exit();
