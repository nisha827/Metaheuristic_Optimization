# Euclidean TSP: constructive heuristics and local search

This module provides a small, reproducible implementation of the travelling-salesperson problem (TSP) for the coordinate instances in this directory.

## Methods

- **Random tour**: reproducible random permutation (`random_tour`).
- **Nearest neighbour**: starts from a selected city and repeatedly visits the closest unvisited city; ties are resolved by city ID.
- **2-opt**: best-improvement edge-reversal search until no improving 2-opt move remains.
- **Perturbation/restarts**: swaps two positions before another 2-opt run to explore a different basin.

The implementation uses explicit city-coordinate mappings, validates tours, avoids module-level mutable state, and does not execute an experiment when imported. It deliberately calls the local-search neighbourhood **2-opt** rather than describing the historical implementation as full 3-opt.

## Run

From the repository root:

```bash
python -m Local_Search.tsp Local_Search/inst-0.tsp --seed 123 --restarts 10
```

Run tests from the repository root:

```bash
python -m pytest Local_Search/tests
```

Only the Python standard library is needed to run the algorithm. Tests use `pytest`.

## Reproducibility and limitations

Set `--seed` to reproduce the nearest-neighbour starting city and perturbations. The objective is the sum of Euclidean distances, with the final city connected back to the first. This is a heuristic, not an exact solver; results depend on the instance and seed. The current implementation focuses on the Local_Search TSP code. The Genetic_Algorithms and SAT experiments remain unchanged and should be reviewed separately before drawing comparisons across methods.
