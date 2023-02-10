''' Import Libraries '''
import pygame
import os
import neat
from random import randrange
import pickle
from scoreBoard import ScoreBoard
from ball import Ball
from paddle import Paddle
from gameState import PongGameState
from configuration import *


# Determines the fitness for a population of NEAT models
def eval_genomes(genomes, config):

    i = 0
    print(len(genomes))
    for genomeID, genome in genomes:
        #with open('winner.pkl', "rb") as f:
        #    genome = pickle.load(f)
        network = neat.nn.FeedForwardNetwork.create(genome, config)
       
        print("genome " + str(i)); i+=1

        # Setup the game
        pygame.init()
        clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 24)
        gameState = PongGameState(); scoreBoard = ScoreBoard(font)
        ball = Ball(); leftPaddle = Paddle('L'); rightPaddle = Paddle('R')

                                            
        ''' Game Loop '''
        games = 10
        while True:
            
            # Check for the user closing the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    break

            output = network.activate([ball.Rect.centery, ball.Rect.centerx, leftPaddle.Rect.centery, rightPaddle.Rect.centery, ball.XVelocity, ball.YVelocity])
            if output[0] > 0.5:
                leftPaddle.MoveUp()
            elif output[0] < -0.5:
                leftPaddle.MoveDown()

            # Move the adversarial AI
            if ball.XVelocity > 0:
                offset = ball.Rect.centery - rightPaddle.Rect.centery
                if offset > 0: # Ball is below paddle
                    rightPaddle.MoveDown()
                else:
                    rightPaddle.MoveUp()
                
            # Update ScoreBoard
            scoreBoard.Update(gameState)
            gameOver = gameState.CheckForWin(games)
            if gameOver:
                ball.Stop()
                pygame.display.quit()
                pygame.quit()
                break
            
            # Move the ball
            ball.Move(leftPaddle, rightPaddle, gameState)

            # Terminate game if too many bounces occur
            if leftPaddle.Returns > 10000:
                print('Game terminated due to excessive length')
                gameState.RightScore = games
                if gameState.LeftScore > games/2:
                    genome.fitness += 1000000

        genome.fitness = leftPaddle.Returns * 10
        genome.fitness += gameState.LeftScore * 1000

        if (gameState.LeftScore == games) and (gameState.RightScore == 0):
            genome.fitness += 1000000
            

        print('fitness = ' + str(genome.fitness))
        print('')

# Runs the training
def run(config_file):
    global maxGenomeFitness
    maxGenomeFitness = 0
    
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    pop = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    # Run for up to 50 generations.
    winner = pop.run(fitness_function = eval_genomes, n = 50)
    
    print(winner)
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close()


    # Show the final result stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    localDir = os.path.dirname(__file__)
    configPath = os.path.join(localDir, 'config-NEAT.txt')
    run(configPath)

