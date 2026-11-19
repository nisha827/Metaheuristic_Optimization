"""Reproducible local-search utilities for Euclidean travelling-salesperson instances.

Instance format: first line is the number of cities; each following line is
``city_id x y``. Tours contain each city ID exactly once and are closed
implicitly when their length is evaluated.
"""
from __future__ import annotations

import argparse
import math
import random
from pathlib import Path
from typing import Mapping, Sequence

Point = tuple[float, float]
Tour = list[int]


def read_instance(filename: str | Path) -> dict[int, Point]:
    """Read and validate a TSPLIB-like coordinate file used in this repository."""
    path = Path(filename)
    with path.open(encoding="utf-8") as handle:
        lines = [line.strip() for line in handle if line.strip()]
    if not lines:
        raise ValueError(f"Empty TSP instance: {path}")
    try:
        expected = int(lines[0])
    except ValueError as exc:
        raise ValueError("The first non-empty line must be the city count") from exc
    cities: dict[int, Point] = {}
    for line_number, line in enumerate(lines[1:], start=2):
        fields = line.split()
        if len(fields) != 3:
            raise ValueError(f"Expected 'city_id x y' on line {line_number}")
        city_id = int(fields[0])
        if city_id in cities:
            raise ValueError(f"Duplicate city id {city_id} on line {line_number}")
        cities[city_id] = (float(fields[1]), float(fields[2]))
    if len(cities) != expected:
        raise ValueError(f"Header declares {expected} cities, found {len(cities)}")
    return cities


def validate_tour(tour: Sequence[int], cities: Mapping[int, Point]) -> None:
    """Raise ValueError unless tour visits every known city exactly once."""
    if len(tour) != len(cities) or set(tour) != set(cities) or len(set(tour)) != len(tour):
        raise ValueError("Tour must contain every city ID exactly once")


def euclidean_distance(city_a: int, city_b: int, cities: Mapping[int, Point]) -> float:
    try:
        ax, ay = cities[city_a]
        bx, by = cities[city_b]
    except KeyError as exc:
        raise ValueError(f"Unknown city ID: {exc.args[0]}") from exc
    return math.hypot(ax - bx, ay - by)


def tour_length(tour: Sequence[int], cities: Mapping[int, Point]) -> float:
    validate_tour(tour, cities)
    if len(tour) < 2:
        return 0.0
    return sum(euclidean_distance(tour[i], tour[(i + 1) % len(tour)], cities)
               for i in range(len(tour)))


def random_tour(cities: Mapping[int, Point], rng: random.Random | None = None) -> Tour:
    rng = rng or random.Random()
    tour = list(cities)
    rng.shuffle(tour)
    return tour


def nearest_neighbour_tour(
    cities: Mapping[int, Point], rng: random.Random | None = None, start: int | None = None
) -> Tour:
    """Build a nearest-neighbour tour; ties are resolved by city ID."""
    if not cities:
        return []
    rng = rng or random.Random()
    remaining = set(cities)
    if start is None:
        start = rng.choice(sorted(remaining))
    if start not in remaining:
        raise ValueError(f"Unknown starting city: {start}")
    tour = [start]
    remaining.remove(start)
    while remaining:
        current = tour[-1]
        next_city = min(remaining, key=lambda city: (euclidean_distance(current, city, cities), city))
        tour.append(next_city)
        remaining.remove(next_city)
    return tour


def two_opt(tour: Sequence[int], cities: Mapping[int, Point]) -> tuple[Tour, float]:
    """Apply best-improvement 2-opt until no improving reversal remains."""
    validate_tour(tour, cities)
    best = list(tour)
    best_cost = tour_length(best, cities)
    improved = True
    while improved:
        improved = False
        n = len(best)
        for i in range(n - 1):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue
                candidate = best[:i + 1] + best[i + 1:j + 1][::-1] + best[j + 1:]
                cost = tour_length(candidate, cities)
                if cost < best_cost - 1e-12:
                    best, best_cost, improved = candidate, cost, True
    return best, best_cost


def perturb(tour: Sequence[int], rng: random.Random | None = None) -> Tour:
    """Return a valid perturbed tour by swapping two distinct positions."""
    result = list(tour)
    if len(result) >= 2:
        rng = rng or random.Random()
        i, j = rng.sample(range(len(result)), 2)
        result[i], result[j] = result[j], result[i]
    return result


def run(instance: Path, seed: int, restarts: int) -> None:
    cities = read_instance(instance)
    rng = random.Random(seed)
    initial = nearest_neighbour_tour(cities, rng=rng)
    best, best_cost = two_opt(initial, cities)
    for _ in range(max(0, restarts)):
        candidate, cost = two_opt(perturb(best, rng), cities)
        if cost < best_cost:
            best, best_cost = candidate, cost
    print(f"Instance: {instance}")
    print(f"Cities: {len(cities)} | seed: {seed} | perturbation restarts: {restarts}")
    print(f"Tour length: {best_cost:.3f}")
    print(f"Tour: {best}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("instance", type=Path, help="Path to an instance file")
    parser.add_argument("--seed", type=int, default=123, help="Random seed")
    parser.add_argument("--restarts", type=int, default=10, help="Perturbation restarts")
    args = parser.parse_args()
    run(args.instance, args.seed, args.restarts)
