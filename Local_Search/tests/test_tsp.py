import random

import pytest

from Local_Search.tsp import (
    euclidean_distance, nearest_neighbour_tour, perturb, read_instance,
    tour_length, two_opt, validate_tour,
)

CITIES = {1: (0.0, 0.0), 2: (1.0, 0.0), 3: (1.0, 1.0), 4: (0.0, 1.0)}


def test_distance_and_closed_tour_length():
    assert euclidean_distance(1, 3, CITIES) == pytest.approx(2 ** 0.5)
    assert tour_length([1, 2, 3, 4], CITIES) == pytest.approx(4.0)


def test_tour_validation_rejects_missing_or_duplicate_city():
    with pytest.raises(ValueError):
        validate_tour([1, 2, 3], CITIES)
    with pytest.raises(ValueError):
        validate_tour([1, 2, 2, 4], CITIES)


def test_nearest_neighbour_includes_each_city_once_and_is_seeded():
    first = nearest_neighbour_tour(CITIES, random.Random(7))
    second = nearest_neighbour_tour(CITIES, random.Random(7))
    assert first == second
    validate_tour(first, CITIES)


def test_two_opt_never_returns_a_worse_tour():
    initial = [1, 3, 2, 4]
    improved, cost = two_opt(initial, CITIES)
    assert cost <= tour_length(initial, CITIES)
    validate_tour(improved, CITIES)


def test_perturb_preserves_city_set():
    changed = perturb([1, 2, 3, 4], random.Random(2))
    assert set(changed) == set(CITIES)
    assert changed != [1, 2, 3, 4]


def test_read_instance_validates_declared_city_count(tmp_path):
    instance = tmp_path / "tiny.tsp"
    instance.write_text("3\n1 0 0\n2 1 0\n3 0 1\n", encoding="utf-8")
    assert read_instance(instance) == {1: (0.0, 0.0), 2: (1.0, 0.0), 3: (0.0, 1.0)}
