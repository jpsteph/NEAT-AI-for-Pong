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
import visualizenets

'''
This file plays the winner for the user using the results of the training script
'''
############################################################

# Change this to True to show the game being played (It may take several minutes to finish the game)
displayGame = True

# Load requried NEAT config
localDir = os.path.dirname(__file__)
configPath = os.path.join(localDir, 'config-NEAT.txt')
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         configPath)
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPath)

# Unpickle saved winner
network = 0
with open('winner.pkl', "rb") as f:
    genome = pickle.load(f)

    # Draw the neural network and save as a .svg
    nodeNames = {-1:'Ball X',-2:'Ball Y',-3:'Left Paddle Y',-4:'Right Paddle Y', -5: 'Ball X Velocity', -6:'Ball Y Velocity'}
    visualizenets.draw_net(config, genome, node_names=nodeNames) 

    # Create the neural network
    network = neat.nn.FeedForwardNetwork.create(genome, config)


# Setup the game
pygame.init()
if displayGame:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
gameState = PongGameState(); scoreBoard = ScoreBoard(font)
ball = Ball(); leftPaddle = Paddle('L'); rightPaddle = Paddle('R')


''' Game Loop '''
while True:
    
    # Check for the user closing the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            break

    # Initalize the neural network for the winner
    network = neat.nn.FeedForwardNetwork.create(genome, config)

    output = network.activate([ball.Rect.centery, ball.Rect.centerx, leftPaddle.Rect.centery, rightPaddle.Rect.centery, ball.XVelocity, ball.YVelocity])
    if output[0] > 0.5:
        leftPaddle.MoveUp()
    elif output[0] < -0.5:
        leftPaddle.MoveDown()

    key = pygame.key.get_pressed()

    if key[pygame.K_w]:
        rightPaddle.MoveUp()
    elif key[pygame.K_s]:
        rightPaddle.MoveDown()

    '''
    # Move the adversarial AI
    if ball.XVelocity > 0:
        offset = ball.Rect.centery - rightPaddle.Rect.centery
        if offset > 0: # Ball is below paddle
            rightPaddle.MoveDown()
        else:
            rightPaddle.MoveUp()
    '''


    # Update ScoreBoard
    scoreBoard.Update(gameState)
    gameOver = gameState.CheckForWin(20)
    if gameOver:
        print('Left Score = ' + str(gameState.LeftScore) + '  , Right Score = ' + str(gameState.RightScore))
        ball.Stop()
        if (displayGame):
            pygame.display.quit()
            pygame.quit()
        break
    
    # Move the ball
    ball.Move(leftPaddle, rightPaddle, gameState)
        
    # Draw to the screen
    if displayGame:
        screen.fill(COLOR_BLACK)
        pygame.draw.line(screen, COLOR_WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
        screen.blit(scoreBoard.LeftScoreSurface, scoreBoard.LeftScoreRect)
        screen.blit(scoreBoard.RightScoreSurface, scoreBoard.RightScoreRect)
        screen.blit(ball.Surface, ball.Rect)
        screen.blit(leftPaddle.Surface, leftPaddle.Rect)
        screen.blit(rightPaddle.Surface, rightPaddle.Rect)
        if gameOver:
            screen.blit(scoreBoard.GameOverSurface, scoreBoard.GameOverRect)
    
        # Update the screen        
        pygame.display.flip()
        clock.tick(400)