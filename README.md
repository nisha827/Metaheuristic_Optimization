# Metaheuristic Optimization

A collection of implementations and experiments exploring metaheuristic optimisation for combinatorial problems, including the Travelling Salesperson Problem (TSP) and Boolean satisfiability (SAT).

The repository contains a refreshed, reproducible local-search workflow for Euclidean TSP alongside historical genetic-algorithm and SAT experiments.

## Repository structure

- `Genetic_Algorithms/` — historical genetic-algorithm experiments for TSP, including individual representations and evolutionary operators.
- `Local_Search/` — Euclidean TSP local search, coordinate instances, and SAT-related experiments.
- `Local_Search/README.md` — detailed documentation for the refreshed TSP implementation.

## Refreshed TSP local-search workflow

The current `Local_Search.tsp` implementation provides:

- **Random tour** construction with a reproducible seed.
- **Nearest neighbour** construction, with deterministic tie-breaking by city ID.
- **Best-improvement 2-opt** to iteratively improve a tour.
- **Perturbation and restarts** to explore alternative local-search basins.

The implementation uses explicit city-coordinate mappings, validates tours, avoids module-level mutable state, and does not launch experiments when imported. The neighbourhood implemented here is 2-opt; it should not be confused with a full 3-opt search.

Run from the repository root:

```bash
python -m Local_Search.tsp Local_Search/inst-0.tsp --seed 123 --restarts 10
```

Run the TSP tests:

```bash
python -m pytest Local_Search/tests
```

The algorithm uses the Python standard library. The test suite uses `pytest`.

## Historical experiments

### Genetic algorithms

The `Genetic_Algorithms/` directory contains earlier experiments with population-based optimisation for TSP, including individual representations and genetic operators such as selection, crossover, and mutation.

These scripts are retained as historical academic work. They are not covered by the refreshed TSP test suite, and their results should not be compared with the current local-search workflow without first standardising the instances, objectives, configurations, and evaluation procedure.

### SAT and local search

The repository also contains historical SAT local-search experiments, including Tabu Search and Novelty+-style approaches. These implementations should be treated as exploratory code; some scripts rely on local problem-instance paths and require configuration before they can be run on another machine.

## Reproducibility and limitations

For the refreshed TSP workflow, set `--seed` to reproduce the nearest-neighbour starting city and perturbations. The objective is the sum of Euclidean distances, including the return edge from the final city to the first. These methods are heuristics, not exact solvers, and outcomes depend on the instance and seed.

The genetic-algorithm and SAT experiments remain separate historical implementations. Further work includes documenting their dependencies and benchmark instances, removing machine-specific paths, adding tests, and comparing methods under consistent experimental conditions.

No performance claims are made here beyond what has been explicitly reproduced and tested.
