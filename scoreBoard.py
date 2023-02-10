import pygame
import os
import neat
from random import randrange
import pickle
from configuration import *

# Handles drawing the score to game screen
class ScoreBoard():
    def __init__(self, font):
        self.LeftScoreCenter = (SCREEN_WIDTH // 2 - SCORE_CENTER_X_OFFSET, SCORE_CENTER_Y_OFFSET)
        self.RightScoreCenter = (SCREEN_WIDTH // 2 + SCORE_CENTER_X_OFFSET, SCORE_CENTER_Y_OFFSET)
        self.Font = pygame.font.SysFont(None, 24)
        self.GameOverSurface = self.Font.render('GAME OVER', True, COLOR_WHITE)
        self.GameOverRect = self.GameOverSurface.get_rect()
        self.GameOverRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    def Update(self, gameState):
        self.LeftScoreSurface = self.Font.render(str(gameState.LeftScore), True, COLOR_WHITE)
        self.RightScoreSurface = self.Font.render(str(gameState.RightScore), True, COLOR_WHITE)
        self.LeftScoreRect = self.LeftScoreSurface.get_rect()
        self.RightScoreRect = self.RightScoreSurface.get_rect()
        self.LeftScoreRect.center = self.LeftScoreCenter
        self.RightScoreRect.center = self.RightScoreCenter