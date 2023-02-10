import scoreBoard
import ball
import paddle
import gameState
from configuration import *

# Tracks the score and winning state for the game
class PongGameState():
    
    def __init__(self):
        self.LeftScore = 0
        self.RightScore = 0
        self.GameOver = False
        
    def CheckForWin(self, scoremax):
        if self.LeftScore >= scoremax or self.RightScore >= scoremax:
            self.GameOver = True
        return self.GameOver