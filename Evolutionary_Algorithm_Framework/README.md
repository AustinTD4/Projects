# Evolutionary Algorithm Framework for Evoman, By Austin Dickerson

The program leverages the Pygame Framework for Evoman, a rendition of the popular Megaman game. The primary objective of the framework is to develop sets of parameters tailored for neural networks, facilitating experiments using a multitude of strategies for Selection, Mutation, and Survival. 

> **Applications:** This tool can be used in any environment where actions can be mapped to a Neural Network in real-time, which consequently produces a performance metric. The algorithms generated represent sets of parameters for a neural network, which can contain additional genotype information, contingent upon the employed strategy.

## Requirements

- **Python**: 3.x
- **Package Manager**: `pip`

## Dependencies

This project relies on the following libraries:

- `Numpy`
- `Pandas`
- `Pygame`
- `scikit-learn`

## Evoman

Evoman features eight unique enemies, each capable of providing a fitness score for the player during gameplay. The scoring considers player life, enemy life, and game time.

### Generalist Algorithm

This experiment aimed to engineer an agent using evolutionary computing, enabling it to overcome all eight enemies, despite only training against 3-4 of them.

## Installation & Setup for Reproducing Evoman Results
1. **Install the required libraries**:
pip install numpy pandas pygame scikit-learn

2. **Clone the repository**:
git clone https://github.com/AustinTD4/Projects.git

3. **Navigate to the Framework Directory**:
cd Evolutionary_Algorithm_Framework

4. **Run the grid search program**:
Grid_Search_Generalist.py

5. **Run the in-depth analysis**:
Test_Selection_Recombination_Mutation.py

### FILES:

- **Demo_Controller.py**: Maps the neural network outputs to commands in Evoman.
- **Grid_Search_Generalist.py**: Runs an experiment where all possible combinations of 3 and 4 enemies are tested for training a generalist agent. Results are saved to csv files.
- **Test_Selection_Recombination.py**: Tests possible selection, recombination, and mutation parameters on on the best performing groups of enemy training combinations.
- **Starter_Culture_Test.py**: Runs an alternate approach where populations were trained against a single boss, merged, and merged again, adding the number of enemies trained on with each layer. Each new population begins with a "Starter Culture", a concatenation of multiple populations evolved against individual enemies respectively. After the final population set is combined, differential evolution is applied for 50 generations.

### FOLDERS:

- **evoman**: Contains the environment and dependencies for evoman, a game based on Megaman, designed in pygame by VU faculty.
- **experiments_evoman**: Contains csv files with the experiment results.

## Robobo Evolutionary Algorithm Controller

This Framework was adapted to develop Genetic Algorithms which control an IRobobo hardware robot. The training process used CappeliaSim to develop Evolutionary Algorithms that allowed the IRobobo to complete tasks, which were tested on hardware IRobobo machines. The primary tasks were collecting "Food" objects, and pushing objects to a location. The IRobobo has 8 Infra-Red Sensors and a mounted camera to survey the environment.

### Files

- **Robobo_Controller_EA**: This file contains the algorithms for training the robot.

## Framework

This framework is designed for modularity, making it adaptable beyond Evoman. To employ this framework for other applications:
1. Modify the simulation to function in the new environment.
2. Adjust the Neural Network shape accordingly.

Evolutionary algorithms will then produce parameters suitable for any given Neural Network shape. This transfer could be done in roughly one hour of changes, depending on the environment.

### Compatibility Matrix

The compatibility matrix for the Evolutionary Algorithm parameters is as follows below. All non-default strategy and recombination parameters are set to `False`. If other strategies of the same category are chosen, they override the default. Only one reproduction strategy and one recombination type can be chosen per experiment. Yellow marks (🟡) indicate a default value, which though present, does not impact experimental behavior.

#### Reproduction Strategies

- Generational Reproduction (Full Replacement)
- Comma Strategy (Over Replacement, Low Survival)
- Steady Reproduction (Only a Subsection of Population Replaced)
- Speciation (Individuals only reproduce within the same Cluster)
- [Evolutionary Programming](http://www.scholarpedia.org/article/Evolutionary_programming)
- [Differential Evolution](https://machinelearningmastery.com/differential-evolution-from-scratch-in-python/)
- [Particle Swarm Optimization](https://machinelearningmastery.com/a-gentle-introduction-to-particle-swarm-optimization/)

#### Recombination Types

- Weighted Average
- Discrete Crossover
- Individual Cross
- Crossover Line
  

| Algorithm/Parameter                     | Mutation Intensity | Mutagenic Temperature | Weighted Avg [Default] | Discrete | Individual Cross | Crossover Line | Curve Parents | Elitism | Threshold | Speciation Frequency | Scaling Factor | Reseed Cycle |
|----------------------------------------|--------------------|-----------------------|------------------------|----------|------------------|----------------|---------------|---------|----------|----------------------|----------------|--------------|
| Generational Reproduction [Default]     | ✅                | ✅                   | ✅                     | ✅      | ✅              | ✅            | ✅           | ✅     | 🟡      | 🟡                  | 🟡            | ✅          |
| Comma Strategy                          | ✅                | ✅                   | ✅                     | ✅      | ✅              | ✅            | ✅           | ✅     | 🟡      | 🟡                  | 🟡            | ✅          |
| Steady Reproduction                     | ✅                | ✅                   | ✅                     | ✅      | ✅              | ✅            | ✅           | ✅     | 🟡      | 🟡                  | 🟡            | ✅          |
| Speciation                              | ✅                | ✅                   | ✅                     | ✅      | ✅              | ✅            | ✅           | 🟡     | ✅      | ✅                  | 🟡            | ❌          |
| Evolutionary Programming                | ✅                | ✅                   | ✅                     | ❌      | ❌              | ❌            | ✅           | 🟡     | 🟡      | 🟡                  | 🟡            | ❌          |
| Differential Evolution                  | 🟡                | 🟡                   | 🟡                     | ✅      | ❌              | ❌            | ❌           | 🟡     | 🟡      | 🟡                  | ✅            | ❌          |
| Particle Swarm Optimization             | 🟡                | 🟡                   | 🟡                     | ❌      | ❌              | ❌            | ❌           | 🟡     | 🟡      | 🟡                  | 🟡            | ❌          |


