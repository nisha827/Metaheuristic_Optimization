# Metaheuristic Optimization

A collection of coursework experiments in metaheuristic optimization, including genetic algorithms for the travelling-salesperson problem (TSP), local-search methods for TSP, and local-search approaches for SAT.

## Current structure

- `Genetic_Algorithms/` — historical genetic-algorithm experiments for TSP.
- `Local_Search/` — Euclidean TSP local search, coordinate instances, and SAT instances.

## Local-search TSP

The `Local_Search/` module contains a reproducible nearest-neighbour construction heuristic, best-improvement 2-opt, and perturbation-based restarts. See [`Local_Search/README.md`](Local_Search/README.md) for the method, assumptions, and commands.

```bash
python -m Local_Search.tsp Local_Search/inst-0.tsp --seed 123 --restarts 10
python -m pytest Local_Search/tests
```

The genetic-algorithm and SAT implementations are retained as historical experiments and are not covered by the current TSP test suite.
