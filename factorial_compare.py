from __future__ import annotations

import math
import timeit
from functools import lru_cache
from typing import Callable, List, Tuple

import matplotlib.pyplot as plt


def factorial_iterative(n: int) -> int:
    """Вычисляет факториал итеративно.

    Args:
        n: неотрицательное целое число.

    Returns:
        Факториал числа n.

    Raises:
        ValueError: если n < 0.
    """
    if n < 0:
        raise ValueError("n must be >= 0")

    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_recursive(n: int) -> int:
    """Рекурсивное вычисление факториала."""
    if n < 0:
        raise ValueError("n must be >= 0")
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)


@lru_cache(maxsize=None)
def factorial_memoized(n: int) -> int:
    """Мемоизированный факториал."""
    if n < 0:
        raise ValueError("n must be >= 0")
    if n <= 1:
        return 1
    return n * factorial_memoized(n - 1)


def measure_time(func: Callable[[int], int], n: int, number: int = 10) -> float:
    """Измеряет среднее время выполнения функции."""
    timer = timeit.Timer(lambda: func(n))
    total_time = timer.timeit(number=number)
    return total_time / number


def compare_factorials(numbers: List[int]) -> Tuple[List[float], List[float], List[float], List[float]]:
    """Сравнивает время выполнения четырёх реализаций факториала."""
    math_times = []
    iterative_times = []
    recursive_times = []
    memoized_times = []

    for n in numbers:
        math_times.append(measure_time(math.factorial, n))
        iterative_times.append(measure_time(factorial_iterative, n))
        recursive_times.append(measure_time(factorial_recursive, n))
        memoized_times.append(measure_time(factorial_memoized, n))

    return math_times, iterative_times, recursive_times, memoized_times


def plot_results(
    numbers: List[int],
    math_times: List[float],
    iterative_times: List[float],
    recursive_times: List[float],
    memoized_times: List[float],
) -> None:
    """Строит график сравнения производительности."""
    plt.figure(figsize=(10, 6))

    plt.plot(numbers, math_times, "o-", label="math.factorial")
    plt.plot(numbers, iterative_times, "s-", label="iterative")
    plt.plot(numbers, recursive_times, "^-", label="recursive")
    plt.plot(numbers, memoized_times, "d-", label="memoized")

    plt.xlabel("n")
    plt.ylabel("time (seconds)")
    plt.title("Factorial implementations performance comparison")
    plt.legend()
    plt.grid(True)
    plt.show()


def main() -> None:
    """Основной запуск программы."""
    numbers = list(range(0, 30, 2))  # 0,2,4,...,28

    math_t, iter_t, rec_t, memo_t = compare_factorials(numbers)

    plot_results(numbers, math_t, iter_t, rec_t, memo_t)


if __name__ == "__main__":
    main()