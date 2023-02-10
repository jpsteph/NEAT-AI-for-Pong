# NEAT-Taught PongAI
The goal of this project is to use NEAT, NeuroEvolution of Augmenting Topologies,
to successfully train an AI to play pong.

The link to the source code for the NEAT library can be found here: https://github.com/CodeReclaimers/neat-python
The documentation for the library can also be found here: https://neat-python.readthedocs.io/en/latest/

Below are descriptions for each file.

## ball.py
This file creates the ball used in our game of Pong.

Within this file are physical properties such as the appearance and the speed of the ball.
Additionally, this file includes code to prevent the ball from clipping into the paddles and getting stuck.
Furthermore, this code contains instructions for what occurs when the ball strikes the paddles or a wall.
Finally, code to determine scoring is included in this file.

## config-NEAT.txt
This file contains initial weights, functions, and properties for the NEAT algorithm.
Essentially this file dictates how NEAT trains our AI.

## configuration.py
This file includes properties to configure the game screen. This includes the size of the screen, its framerate, as well as the size and speed of paddles.
Included in this file are also color values and the score zone offsets.

## gameState.py
This file simply tracks the game score and determines if someone wins.

## paddle.py
This file creates the paddle used in our game of Pong.

This file contains code that sets the colors, sizes, and speeds of the paddles using values in 'configuration.py'.
It also contains code to properly position the paddles and control their speeds.

## scoreBoard.py
This file draws the scoreboard using values in 'configuration.py'.
It then updates the scoreboard when points are scored.

## train.py
This file trains the pong AI.

Within this file the genome for the NEAT algorithm is created and updated.
This file also sets up and maintains the game using 'ball.py', 'paddle.py', 'scoreBoard.py', and 'gameState.py'. 
If the game takes too long it is terminated.
While the game is running, the adverserial AI is programed through this file.
Results are also outputted to the terminal through this file.

## winner.pkl
This file contains the pickled genome of the winner from the training program ran through 'train.py'.

## winner.py
This file uses the genome located in 'winner.pkl' to run a game with a winning genome.
The purpose of this is to show the final results of 'train.py' without running the full-length training program.

## visualizenets.py
The code to display a diagram of a neural network is here.  This was taken from the tutorial for the open source NEAT-Python library.  This code requires
the Graphviz library and executable to be installed and added to the system path on the machine running it.


