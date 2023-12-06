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
- Results
- Contributors

## Installation

To get started with this project, clone the repository to your local machine:

```conda
git clone https://github.com/AustinTD4/Projects.git
```

Make sure you have Python installed on your system. The required dependencies can be installed using:

pip install numpy colorama tqdm

## Usage

### Training the AI

To train the AI, run the explore command with the number of games and the filename to be saved:

```python
connectFour.explore(10000000, '{filename}')
```

### Testing the AI

After training, you can test the AI's performance, selecting the number of test games and the AI's pkl file:

```python
connectFour.testPerformance(1000, '{filename}')
```

### Human vs AI Gameplay

Play against the trained AI by loading the pkl file from training:

```python
connectFour.humanPlay('{filename}')
```

### Visualizing Performance

Visualize the decision-making process of the AI by watching one game unfold with win probabilities for upcoming actions:

```python
connectFour.visualizePerformance('{filename}')
```

### Advanced Train

Create a version of the game where the opponent followis its own policy to maximize reward and also makes exploratory decisions:

```python
connectFourAdvanced = gameBoard(advancedTrain=True)
connectFourAdvanced.explore(10000000, f'{filename}_Advanced', previousPolicy='{filename}', exploitativeSampling=True)
```

## Results

Utilizing the standard training protocol against a random opponent converged to a 96.5% win rate for the on policy player. In the advanced training setting, both players followed their own policy anbd win rate stayed consistently between 45%-55% during training. After 10 million simulated games, the resulting AI player could reliably beat human opponents.

## Contributors

- Austin Dickerson
