# Evolutionary Algorithm Framework for Evoman, By Austin Dickerson

The program leverages the Pygame Framework for Evoman, a rendition of the popular Megaman game. The primary objective of the framework is to develop sets of parameters tailored for neural networks, facilitating experiments using a multitude of strategies for Selection, Mutation, and Survival. 

> **Applications:** This tool can be used in any environment where actions can be mapped to a Neural Network in real-time, which consequently produces a performance metric. The algorithms generated represent sets of parameters for a neural network, which can contain additional genotype information, contingent upon the employed strategy.

## Framework

This framework is designed for modularity, making it adaptable beyond Evoman. To employ this framework for other applications:
1. Modify the simulation to function in the new environment.
2. Adjust the Neural Network shape accordingly.

Evolutionary algorithms will then produce parameters suitable for any given Neural Network shape.

## Requirements

- **Python**: 3.x
- **Package Manager**: `pip`

## Dependencies

This project relies on the following libraries:

- `Numpy`
- `Pandas`
- `Pygame`

## Installation & Setup for Reproducing Evoman Experiments

1. **Install the required libraries**:
pip install numpy pandas pygame

2. **Clone the repository**:
git clone https://github.com/AustinTD4/Projects.git

3. **Navigate to the Framework Directory**:
cd Evolutionary_Algorithm_Framework

4. **Run the grid search program**:
Grid_Search_Generalist.py

5. **Run the in-depth analysis**:
Tuning_Generalist.py


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

## Evoman

Evoman features eight unique enemies, each capable of providing a fitness score for the player during gameplay. The scoring considers player life, enemy life, and game time.

### Generalist Algorithm

This experiment aimed to engineer an agent using evolutionary computing, enabling it to overcome all eight enemies, despite only training against 3-4 of them.

**Procedure:**

1. **Grid Search through enemy combinations**
   - Investigate all enemy combinations for 20 generations using an efficient approach [Generational Reproduction, Weighted Avg, Curve Parents, Elitism=1].
   - Analyze outcomes and cherry-pick the optimal combinations for in-depth testing.
