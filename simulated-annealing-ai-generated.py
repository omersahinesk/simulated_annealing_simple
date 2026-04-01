import math
import random
import time
from dataclasses import dataclass
from typing import Callable, List, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np


Route = List[int]
MoveFn = Callable[[Route, random.Random], Route]


@dataclass
class SAConfig:
    matrix_min: int = 1
    matrix_max: int = 100
    matrix_size: int = 20
    initial_temperature: float = 1000.0
    final_temperature: float = 1.0
    cooling_rate: float = 0.995
    iterations_per_temperature: int = 200
    max_steps: int | None = None
    seed: int | None = None


@dataclass
class SAResult:
    best_route: Route
    best_cost: int
    initial_route: Route
    initial_cost: int
    iterations: int
    elapsed_seconds: float
    improvement_history: List[int]
    best_history: List[int]


def create_distance_matrix(
    min_value: int,
    max_value: int,
    size: int,
    rng: random.Random,
    symmetric: bool = False,
) -> np.ndarray:
    if size < 2:
        raise ValueError("matrix_size en az 2 olmalı.")
    if min_value > max_value:
        raise ValueError("matrix_min, matrix_max'tan büyük olamaz.")

    matrix = np.zeros((size, size), dtype=int)

    if symmetric:
        for i in range(size):
            for j in range(i + 1, size):
                value = rng.randint(min_value, max_value)
                matrix[i, j] = value
                matrix[j, i] = value
    else:
        for i in range(size):
            for j in range(size):
                if i != j:
                    matrix[i, j] = rng.randint(min_value, max_value)

    return matrix


def route_cost(matrix: np.ndarray, route: Sequence[int]) -> int:
    total = 0
    size = len(route)

    for i in range(size):
        total += int(matrix[route[i], route[(i + 1) % size]])

    return total


def move_swap(route: Route, rng: random.Random) -> Route:
    new_route = route.copy()
    i, j = sorted(rng.sample(range(len(new_route)), 2))
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route


def move_insert(route: Route, rng: random.Random) -> Route:
    new_route = route.copy()
    i, j = rng.sample(range(len(new_route)), 2)
    city = new_route.pop(i)
    new_route.insert(j, city)
    return new_route


def move_reverse(route: Route, rng: random.Random) -> Route:
    new_route = route.copy()
    i, j = sorted(rng.sample(range(len(new_route)), 2))
    new_route[i : j + 1] = reversed(new_route[i : j + 1])
    return new_route


def acceptance_probability(current_cost: int, candidate_cost: int, temperature: float) -> float:
    delta = candidate_cost - current_cost

    if delta <= 0:
        return 1.0

    return math.exp(-delta / temperature)


def choose_neighbor(route: Route, rng: random.Random, moves: Sequence[MoveFn]) -> Route:
    move = rng.choice(moves)
    return move(route, rng)


def simulated_annealing(matrix: np.ndarray, config: SAConfig) -> SAResult:
    rng = random.Random(config.seed)
    moves: Tuple[MoveFn, ...] = (move_swap, move_insert, move_reverse)

    current_route = rng.sample(range(len(matrix)), len(matrix))
    current_cost = route_cost(matrix, current_route)

    best_route = current_route.copy()
    best_cost = current_cost

    initial_route = current_route.copy()
    initial_cost = current_cost

    improvement_history: List[int] = []
    best_history: List[int] = [best_cost]

    temperature = config.initial_temperature
    iterations = 0
    start_time = time.perf_counter()

    while temperature > config.final_temperature:
        for _ in range(config.iterations_per_temperature):
            if config.max_steps is not None and iterations >= config.max_steps:
                elapsed = time.perf_counter() - start_time
                return SAResult(
                    best_route=best_route,
                    best_cost=best_cost,
                    initial_route=initial_route,
                    initial_cost=initial_cost,
                    iterations=iterations,
                    elapsed_seconds=elapsed,
                    improvement_history=improvement_history,
                    best_history=best_history,
                )

            candidate_route = choose_neighbor(current_route, rng, moves)
            candidate_cost = route_cost(matrix, candidate_route)

            ap = acceptance_probability(current_cost, candidate_cost, temperature)
            if rng.random() < ap:
                current_route = candidate_route
                current_cost = candidate_cost

            if current_cost < best_cost:
                best_route = current_route.copy()
                best_cost = current_cost
                improvement_history.append(best_cost)

            best_history.append(best_cost)
            iterations += 1

        temperature *= config.cooling_rate

    elapsed = time.perf_counter() - start_time

    return SAResult(
        best_route=best_route,
        best_cost=best_cost,
        initial_route=initial_route,
        initial_cost=initial_cost,
        iterations=iterations,
        elapsed_seconds=elapsed,
        improvement_history=improvement_history,
        best_history=best_history,
    )


def print_summary(matrix: np.ndarray, result: SAResult) -> None:
    print("\nMesafe Matrisi:")
    print(matrix)

    print("\nBaşlangıç çözümü:")
    print(result.initial_route)
    print("Başlangıç maliyeti:", result.initial_cost)

    print("\nEn iyi çözüm:")
    print(result.best_route)
    print("En iyi maliyet:", result.best_cost)

    print("\nİyileşme:", result.initial_cost - result.best_cost)
    print("Toplam iterasyon:", result.iterations)
    print("Çalışma süresi (sn):", round(result.elapsed_seconds, 4))


def plot_progress(result: SAResult) -> None:
    plt.figure(figsize=(10, 5))
    plt.plot(result.best_history)
    plt.title("Simulated Annealing - Best Cost History")
    plt.xlabel("Iteration")
    plt.ylabel("Best Cost")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def get_user_config() -> SAConfig:
    matrix_min = int(input("Matris'in en küçük değeri: "))
    matrix_max = int(input("Matris'in en büyük değeri: "))
    matrix_size = int(input("Matris boyutu: "))
    initial_temperature = float(input("Başlangıç sıcaklığı: "))
    iterations_per_temperature = int(input("Her sıcaklık için iterasyon sayısı: "))

    return SAConfig(
        matrix_min=matrix_min,
        matrix_max=matrix_max,
        matrix_size=matrix_size,
        initial_temperature=initial_temperature,
        final_temperature=1.0,
        cooling_rate=0.995,
        iterations_per_temperature=iterations_per_temperature,
        seed=None,
    )


def main() -> None:
    config = get_user_config()
    rng = random.Random(config.seed)

    matrix = create_distance_matrix(
        min_value=config.matrix_min,
        max_value=config.matrix_max,
        size=config.matrix_size,
        rng=rng,
        symmetric=False,
    )

    result = simulated_annealing(matrix, config)
    print_summary(matrix, result)
    plot_progress(result)


if __name__ == "__main__":
    main()
