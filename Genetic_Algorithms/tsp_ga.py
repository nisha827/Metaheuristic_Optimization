"""A small, reproducible genetic algorithm for Euclidean TSP instances.

The original coursework implementation remains in TSP.py. This module is the
maintained, import-safe implementation used by the accompanying tests.
"""
from __future__ import annotations

import math
import random
from collections.abc import Mapping, Sequence

Point = tuple[float, float]
Tour = list[int]


def validate_tour(tour: Sequence[int], cities: Mapping[int, Point]) -> None:
    if len(tour) != len(cities) or len(set(tour)) != len(tour) or set(tour) != set(cities):
        raise ValueError("A tour must visit every city exactly once")


def tour_length(tour: Sequence[int], cities: Mapping[int, Point]) -> float:
    validate_tour(tour, cities)
    if len(tour) < 2:
        return 0.0
    return sum(
        math.dist(cities[tour[i]], cities[tour[(i + 1) % len(tour)]])
        for i in range(len(tour))
    )


def order_crossover(parent_a: Sequence[int], parent_b: Sequence[int], rng: random.Random) -> Tour:
    """Order crossover (OX); returns a valid permutation of the parent genes."""
    if len(parent_a) != len(parent_b) or set(parent_a) != set(parent_b):
        raise ValueError("Parents must contain the same genes")
    size = len(parent_a)
    if size < 2:
        return list(parent_a)
    left, right = sorted(rng.sample(range(size), 2))
    child: list[int | None] = [None] * size
    child[left:right + 1] = parent_a[left:right + 1]
    used = set(child[left:right + 1])
    fill = [gene for offset in range(size) for gene in
            (parent_b[(right + 1 + offset) % size],) if gene not in used]
    positions = list(range(right + 1, size)) + list(range(0, left))
    for position, gene in zip(positions, fill):
        child[position] = gene
    result = [gene for gene in child if gene is not None]
    if len(result) != size:
        raise RuntimeError("Crossover failed to produce a complete tour")
    return result


def swap_mutation(tour: Sequence[int], rng: random.Random, rate: float) -> Tour:
    if not 0.0 <= rate <= 1.0:
        raise ValueError("Mutation rate must be between 0 and 1")
    result = list(tour)
    if len(result) > 1 and rng.random() < rate:
        i, j = rng.sample(range(len(result)), 2)
        result[i], result[j] = result[j], result[i]
    return result


class GeneticTSPSolver:
    """Tournament-selected GA with OX, swap mutation and elitism."""

    def __init__(
        self, population_size: int = 100, generations: int = 300,
        mutation_rate: float = 0.1, tournament_size: int = 3,
        elite_size: int = 1, seed: int | None = None,
    ) -> None:
        if population_size < 2:
            raise ValueError("population_size must be at least 2")
        if generations < 0:
            raise ValueError("generations cannot be negative")
        if tournament_size < 1 or tournament_size > population_size:
            raise ValueError("tournament_size must be in [1, population_size]")
        if elite_size < 0 or elite_size >= population_size:
            raise ValueError("elite_size must be in [0, population_size)")
        if not 0.0 <= mutation_rate <= 1.0:
            raise ValueError("mutation_rate must be between 0 and 1")
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elite_size = elite_size
        self.rng = random.Random(seed)

    def _select(self, population: list[Tour], costs: list[float]) -> Tour:
        """Tournament selection for a minimisation objective."""
        candidates = self.rng.sample(range(len(population)), self.tournament_size)
        winner = min(candidates, key=lambda index: costs[index])
        return population[winner]

    def solve(self, cities: Mapping[int, Point]) -> tuple[Tour, float]:
        if not cities:
            raise ValueError("At least one city is required")
        if any(len(point) != 2 or not all(math.isfinite(v) for v in point) for point in cities.values()):
            raise ValueError("City coordinates must be finite 2D points")

        city_ids = list(cities)
        population = []
        for _ in range(self.population_size):
            candidate = city_ids.copy()
            self.rng.shuffle(candidate)
            population.append(candidate)

        costs = [tour_length(tour, cities) for tour in population]
        best_index = min(range(len(costs)), key=costs.__getitem__)
        best_tour, best_cost = population[best_index].copy(), costs[best_index]

        for _ in range(self.generations):
            ranked = sorted(zip(costs, population), key=lambda item: item[0])
            next_population = [tour.copy() for _, tour in ranked[:self.elite_size]]
            while len(next_population) < self.population_size:
                parent_a = self._select(population, costs)
                parent_b = self._select(population, costs)
                child = order_crossover(parent_a, parent_b, self.rng)
                child = swap_mutation(child, self.rng, self.mutation_rate)
                next_population.append(child)
            population = next_population
            costs = [tour_length(tour, cities) for tour in population]
            generation_best = min(range(len(costs)), key=costs.__getitem__)
            if costs[generation_best] < best_cost:
                best_tour = population[generation_best].copy()
                best_cost = costs[generation_best]

        validate_tour(best_tour, cities)
        return best_tour, best_cost
