# Genetic Algorithms: Maintained TSP Implementation

The original coursework implementation is retained in `TSP.py` and `Individual.py`.
For new experiments, use `tsp_ga.py`: an import-safe implementation with
minimisation-aware tournament selection, order crossover, swap mutation,
elitism, deterministic seeding and explicit tour validation.

## Run tests

From the repository root:

```bash
python -m pip install pytest
python -m pytest Genetic_Algorithms/tests
```

## Use

```python
from Genetic_Algorithms.tsp_ga import GeneticTSPSolver

cities = {1: (0.0, 0.0), 2: (1.0, 0.0), 3: (1.0, 1.0), 4: (0.0, 1.0)}
solver = GeneticTSPSolver(population_size=100, generations=300, seed=42)
best_tour, best_length = solver.solve(cities)
print(best_tour, best_length)
```

This is a baseline implementation, not a claim of optimality. Compare repeated
seeded runs and report solution quality, runtime and variability before drawing
conclusions about algorithm performance.
