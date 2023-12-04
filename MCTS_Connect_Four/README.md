# Connect Four AI with Monte Carlo Tree Search

This project implements a Connect Four game AI using Monte Carlo Tree Search (MCTS) in Python. It various modes including AI training, testing, human vs AI gameplay, and performance visualization, and advanced training.

## Table of Contents

- Installation
- Usage
  - Training the AI
  - Testing the AI
  - Human vs AI Gameplay
  - Visualizing Performance
  - Advanced Train
- Contributors

## Installation

To get started with this project, clone the repository to your local machine:

git clone https://github.com/AustinTD4/Projects.git
cd Projects
cd MCTS_Connect_Four

Make sure you have Python installed on your system. The required dependencies can be installed using:

pip install numpy colorama tqdm

## Usage

### Training the AI

To train the AI, run the explore command with the number of games and the filename to be saved:

connectFour.explore(10000000, '{filename}')

### Testing the AI

After training, you can test the AI's performance, selecting the number of test games and the AI's pkl file:

connectFour.testPerformance(1000, '{filename}')

### Human vs AI Gameplay

Play against the trained AI by loading the pkl file from training:

connectFour.humanPlay('{filename}')

### Visualizing Performance

Visualize the decision-making process of the AI by watching one game unfold with win probabilities for upcoming actions:

connectFour.visualizePerformance('{filename}')

### Advanced Train

Create a version of the game where the opponent used to train against is playing with a previously developed AI:

connectFourAdvanced = gameBoard(advancedTrain=True)
connectFourAdvanced.explore(10000000, f'{filename}_Advanced', previousPolicy='{filename}', exploitativeSampling=True)

## Contributors

- Austin Dickerson
