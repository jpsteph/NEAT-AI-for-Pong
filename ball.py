import pygame
import os
import neat
from random import randrange
import pickle
from configuration import *

# Handles the ball and its collisions
class Ball(pygame.sprite.Sprite):
    
    def __init__(self):
        
        self.Color = COLOR_WHITE
        self.Width = 5
        self.XVelocity = -1
        self.YVelocity = -1
        self.Surface = pygame.Surface((self.Width, self.Width))
        self.Surface.fill(self.Color)
        self.Rect = self.Surface.get_rect()
        self.Rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
    def Move(self, leftPaddle, rightPaddle, gameState):
        
        # Prevent clipping issues
        if self.Rect.top < 0:
            self.Rect.top = 0
        if self.Rect.bottom > SCREEN_HEIGHT:
            self.Rect.bottom = SCREEN_HEIGHT
        

        # Prevent y velocity from becoming zero because the ball can get stuck
        if self.YVelocity == 0:
            self.YVelocity = randrange(-1, 1)

        # Correct out of bounds velocity
        if abs(self.XVelocity) > 3:
            self.XVelocity = 3 * self.XVelocity / abs(self.XVelocity)
        elif abs(self.YVelocity) > 3:
            self.YVelocity = 3 * self.YVelocity / abs(self.YVelocity)

        # Check for wall collisions
        if (self.Rect.top <= 0) or (self.Rect.bottom >= SCREEN_HEIGHT):
            self.YVelocity *= -1
            
        # Check for paddle collisions
        if leftPaddle.Rect.colliderect(self.Rect) or rightPaddle.Rect.colliderect(self.Rect):
            self.XVelocity *= -1
            if leftPaddle.Rect.colliderect(self.Rect):
                leftPaddle.Returns += 1
                self.Rect.left = leftPaddle.Rect.right
                if self.Rect.centery > leftPaddle.Rect.centery + PADDLE_HEIGHT // 6:
                    self.XVelocity = (1 + abs(self.XVelocity)) * self.XVelocity / abs(self.XVelocity)
                    self.YVelocity = (1 + abs(self.YVelocity)) * self.YVelocity / abs(self.YVelocity)
                elif self.Rect.centery < leftPaddle.Rect.centery - PADDLE_HEIGHT // 6:
                    self.XVelocity = (1 + abs(self.XVelocity)) * self.XVelocity / abs(self.XVelocity)
                    self.YVelocity = (1 + abs(self.YVelocity)) * self.YVelocity / abs(self.YVelocity)
                else:
                    self.XVelocity = self.XVelocity / abs(self.XVelocity)
                    self.YVelocity = self.YVelocity / abs(self.YVelocity)
            if rightPaddle.Rect.colliderect(self.Rect):
                rightPaddle.Returns += 1
                self.Rect.right = rightPaddle.Rect.left
                if self.Rect.centery > rightPaddle.Rect.centery + PADDLE_HEIGHT // 6:
                    self.XVelocity = (1 + abs(self.XVelocity)) * self.XVelocity / abs(self.XVelocity)
                    self.YVelocity = (1 + abs(self.YVelocity)) * self.YVelocity / abs(self.YVelocity)
                elif self.Rect.centery < rightPaddle.Rect.centery - PADDLE_HEIGHT // 6:
                    self.YVelocity = (1 + abs(self.YVelocity)) * self.YVelocity / abs(self.YVelocity)
                    self.XVelocity = (1 + abs(self.XVelocity)) * self.XVelocity / abs(self.XVelocity)
                else:
                    self.XVelocity = self.XVelocity / abs(self.XVelocity)
                    self.YVelocity = self.YVelocity / abs(self.YVelocity)
            
        # Check for scoring
        if self.Rect.right <= 0:
            self.Reset()
            gameState.RightScore += 1
            rightPaddle.Score += 1
        elif self.Rect.left >= SCREEN_WIDTH:
            self.Reset()
            gameState.LeftScore += 1
            leftPaddle.Score += 1

        # Update ball position
        self.Rect.left += self.XVelocity
        self.Rect.top += self.YVelocity
    
    def Reset(self):
        
        self.Rect.center = (SCREEN_WIDTH // 2, randrange(0, SCREEN_HEIGHT))
        self.XVelocity *= -1 / abs(self.XVelocity)
        self.YVelocity *= -1 / abs(self.YVelocity)
        
    def Stop(self):
        
        self.XVelocity = 0
        self.YVelocity = 0
        