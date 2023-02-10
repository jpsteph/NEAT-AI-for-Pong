''' Import Libraries '''
import pygame
import os
import neat
from random import randrange
import pickle
from configuration import *

# Handles the movement of the paddles
class Paddle(pygame.sprite.Sprite):
    
    def __init__(self, side):
        if side == 'L':
            self.Color = COLOR_BLUE
        else:
            self.Color = COLOR_RED
        self.Width = PADDLE_WIDTH
        self.Height = PADDLE_HEIGHT
        self.Speed = PADDLE_SPEED
        self.Surface = pygame.Surface((self.Width, self.Height))
        self.Surface.fill(self.Color)
        self.Rect = self.Surface.get_rect()
        self.Returns = 0
        self.Score = 0
        self.MovedUp = False
        self.MovedDown = False
        self.FitScore = 0

        if side == 'L':
            self.Rect.center = (20, SCREEN_HEIGHT // 2)
        else:
            self.Rect.center = (SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2)
            
    def MoveUp(self):
        self.MovedUp = True
        if self.Rect.top > 1:
            self.Rect.top -= self.Speed
    
    def MoveDown(self):
        self.MovedDown = True
        if self.Rect.bottom < SCREEN_HEIGHT:
            self.Rect.bottom += self.Speed