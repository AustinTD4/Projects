A framework to develop sets of parameters for a neural network.

Compatability matrix of the Evolutionary Algorithm parameters is listed below. All parameters start set to False, expect the defaults. Choosing any other option will overule the default.

| Algorithm/Parameter                     | Mutation Intensity | Mutagenic Temperature | Weighted Avg [Default] | Discrete | Individual Cross | Crossover Line | Curve Parents | Elitism | Threshold | Speciation Frequency | Scaling Factor |
|----------------------------------------|--------------------|-----------------------|------------------------|----------|------------------|----------------|---------------|---------|----------|----------------------|----------------|
| Generational Reproduction [Default]     | ✅                | ✅                   | ✅                     | ✅      | ✅              | ✅            | ✅           | ✅     | ❌      | ❌                  | ❌            |
| Comma Strategy                          | ✅                | ✅                   | ✅                     | ✅      | ✅              | ✅            | ✅           | ✅     | ❌      | ❌                  | ❌            |
| Steady Reproduction                     | ✅                | ✅                   | ✅                     | ✅      | ✅              | ✅            | ✅           | ✅     | ❌      | ❌                  | ❌            |
| Speciation                              | ✅                | ✅                   | ✅                     | ✅      | ✅              | ✅            | ❌           | ❌     | ✅      | ✅                  | ❌            |
| Evolutionary Programming                | ✅                | ✅                   | ❌                     | ❌      | ❌              | ❌            | ✅           | ❌     | ❌      | ❌                  | ❌            |
| Differential Evolution                  | ❌                | ❌                   | ❌                     | ✅      | ❌              | ❌            | ❌           | ❌     | ❌      | ❌                  | ✅            |
