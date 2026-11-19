import random
import pytest

from Genetic_Algorithms.tsp_ga import (
    GeneticTSPSolver, order_crossover, swap_mutation, tour_length, validate_tour,
)

CITIES = {1: (0.0, 0.0), 2: (1.0, 0.0), 3: (1.0, 1.0), 4: (0.0, 1.0)}


def test_tour_length_closes_cycle():
    assert tour_length([1, 2, 3, 4], CITIES) == pytest.approx(4.0)


def test_validation_rejects_duplicate_and_missing_cities():
    with pytest.raises(ValueError):
        validate_tour([1, 2, 2, 4], CITIES)


def test_order_crossover_always_returns_valid_permutation():
    rng = random.Random(42)
    a, b = [1, 2, 3, 4, 5], [3, 5, 1, 4, 2]
    for _ in range(100):
        child = order_crossover(a, b, rng)
        assert len(child) == len(set(child)) == 5
        assert set(child) == set(a)


def test_swap_mutation_preserves_permutation():
    result = swap_mutation([1, 2, 3, 4], random.Random(2), 1.0)
    assert sorted(result) == [1, 2, 3, 4]


def test_solver_is_reproducible_and_returns_valid_tour():
    kwargs = dict(population_size=30, generations=40, seed=123)
    first = GeneticTSPSolver(**kwargs).solve(CITIES)
    second = GeneticTSPSolver(**kwargs).solve(CITIES)
    assert first == second
    validate_tour(first[0], CITIES)
    assert first[1] == pytest.approx(tour_length(first[0], CITIES))


def test_solver_rejects_invalid_configuration():
    with pytest.raises(ValueError):
        GeneticTSPSolver(population_size=1)
