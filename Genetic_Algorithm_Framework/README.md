A framework to develop sets of parameters for a neural network.

A Compatability matrix of the Evolutionary Algorithm parameters is listed below. All parameters start set to False, except the defaults. Choosing other options will overule the default. Only one reproduction strategy and recombination type can be selected for an experiment.

Reproduction Parameters: [Generational Reproduction, Comma Strategy, Steady Reproduction, Speciation, Evolutionary Programming, Differential Evolution, Particle Swarm Optimization]

| Algorithm/Parameter                     | Mutation Intensity | Mutagenic Temperature | Weighted Avg [Default] | Discrete | Individual Cross | Crossover Line | Curve Parents | Elitism | Threshold | Speciation Frequency | Scaling Factor | Reseed Cycle |
|----------------------------------------|--------------------|-----------------------|------------------------|----------|------------------|----------------|---------------|---------|----------|----------------------|----------------|--------------|
| Generational Reproduction [Default]     | ✅                | ✅                   | ✅                     | ✅      | ✅              | ✅            | ✅           | ✅     | ❌      | ❌                  | ❌            | ✅          |
| Comma Strategy                          | ✅                | ✅                   | ✅                     | ✅      | ✅              | ✅            | ✅           | ✅     | ❌      | ❌                  | ❌            | ✅          |
| Steady Reproduction                     | ✅                | ✅                   | ✅                     | ✅      | ✅              | ✅            | ✅           | ✅     | ❌      | ❌                  | ❌            | ✅          |
| Speciation                              | ✅                | ✅                   | ✅                     | ✅      | ✅              | ✅            | ❌           | ❌     | ✅      | ✅                  | ❌            | ❌          |
| Evolutionary Programming                | ✅                | ✅                   | ❌                     | ❌      | ❌              | ❌            | ✅           | ❌     | ❌      | ❌                  | ❌            | ❌          |
| Differential Evolution                  | ❌                | ❌                   | ❌                     | ✅      | ❌              | ❌            | ❌           | ❌     | ❌      | ❌                  | ✅            | ❌          |
