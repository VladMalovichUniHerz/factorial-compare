"""
Модуль с тестами для проверки реализаций факториала.
Использует pytest для автоматического тестирования.
"""

import pytest
import math
import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(__file__))

# Импортируем функции из основного модуля
from factorial_compare import (
    factorial_iterative,
    factorial_recursive,
    factorial_memoized,
    measure_time,
    compare_factorials
)


# ============================================================
# Тесты для проверки корректности вычислений
# ============================================================

class TestFactorialCorrectness:
    """Тесты правильности вычисления факториала."""

    @pytest.mark.parametrize("n,expected", [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120),
        (6, 720),
        (7, 5040),
        (10, 3628800),
    ])
    def test_iterative_factorial(self, n, expected):
        """Проверка итеративной реализации."""
        result = factorial_iterative(n)
        assert result == expected
        assert result == math.factorial(n)

    @pytest.mark.parametrize("n,expected", [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120),
        (10, 3628800),
    ])
    def test_recursive_factorial(self, n, expected):
        """Проверка рекурсивной реализации."""
        result = factorial_recursive(n)
        assert result == expected
        assert result == math.factorial(n)

    @pytest.mark.parametrize("n,expected", [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120),
        (10, 3628800),
    ])
    def test_memoized_factorial(self, n, expected):
        """Проверка мемоизированной реализации."""
        # Очищаем кэш перед тестом
        factorial_memoized.cache_clear()
        result = factorial_memoized(n)
        assert result == expected
        assert result == math.factorial(n)

    def test_all_implementations_match(self):
        """Проверка, что все реализации дают одинаковые результаты."""
        test_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15]

        for n in test_numbers:
            expected = math.factorial(n)
            assert factorial_iterative(n) == expected, f"Ошибка в итеративной для n={n}"
            assert factorial_recursive(n) == expected, f"Ошибка в рекурсивной для n={n}"
            # Очищаем кэш для чистоты теста
            factorial_memoized.cache_clear()
            assert factorial_memoized(n) == expected, f"Ошибка в мемоизированной для n={n}"


# ============================================================
# Тесты для проверки обработки ошибок
# ============================================================

class TestFactorialErrors:
    """Тесты обработки ошибочных входных данных."""

    @pytest.mark.parametrize("func", [
        factorial_iterative,
        factorial_recursive,
        factorial_memoized
    ])
    @pytest.mark.parametrize("invalid_n", [-1, -5, -10])
    def test_negative_numbers_raise_value_error(self, func, invalid_n):
        """Проверка, что отрицательные числа вызывают ValueError."""
        with pytest.raises(ValueError, match="n must be >= 0"):
            func(invalid_n)

    def test_memoized_cache_clear(self):
        """Проверка очистки кэша мемоизированной функции."""
        # Очищаем кэш
        factorial_memoized.cache_clear()
        assert factorial_memoized.cache_info().currsize == 0

        # Вычисляем значение
        factorial_memoized(10)
        assert factorial_memoized.cache_info().currsize > 0

        # Очищаем снова
        factorial_memoized.cache_clear()
        assert factorial_memoized.cache_info().currsize == 0


# ============================================================
# Тесты для функции measure_time
# ============================================================

class TestMeasureTime:
    """Тесты для функции измерения времени."""

    def test_measure_time_returns_float(self):
        """Проверка, что measure_time возвращает число с плавающей точкой."""
        result = measure_time(math.factorial, 10)
        assert isinstance(result, float)
        assert result > 0

    def test_measure_time_accuracy(self):
        """Проверка, что время выполнения правдоподобно."""
        # Быстрая операция должна занимать мало времени
        fast_time = measure_time(lambda x: x + 1, 10, number=1000)
        assert 0 < fast_time < 0.01  # меньше 10 миллисекунд

        # Более медленная операция должна занимать больше времени
        slow_time = measure_time(factorial_recursive, 20, number=10)
        assert slow_time > 0

    def test_compare_factorials_structure(self):
        """Проверка структуры возвращаемых данных compare_factorials."""
        test_numbers = [0, 5, 10]
        result = compare_factorials(test_numbers)

        # Должно быть 4 списка
        assert len(result) == 4

        # Каждый список должен иметь длину, равную количеству тестовых чисел
        for times_list in result:
            assert len(times_list) == len(test_numbers)

        # Все значения должны быть числами с плавающей точкой
        math_times, iter_times, rec_times, memo_times = result
        assert all(isinstance(t, float) for t in math_times)
        assert all(isinstance(t, float) for t in iter_times)
        assert all(isinstance(t, float) for t in rec_times)
        assert all(isinstance(t, float) for t in memo_times)


# ============================================================
# Тесты производительности
# ============================================================

class TestPerformance:
    """Тесты производительности реализаций."""

    def test_iterative_vs_recursive(self):
        """Сравнение производительности итеративной и рекурсивной версий."""
        n = 20

        iter_time = measure_time(factorial_iterative, n, number=50)
        rec_time = measure_time(factorial_recursive, n, number=50)

        print(f"\nИтеративная время: {iter_time:.8f} сек")
        print(f"Рекурсивная время: {rec_time:.8f} сек")

        # Просто проверяем, что время измерено корректно
        assert iter_time > 0
        assert rec_time > 0

        # Выводим соотношение для информации
        if rec_time > iter_time:
            print(f"Итеративная быстрее в {rec_time / iter_time:.2f} раза")

    def test_memoization_effect(self):
        """Проверка, что мемоизация ускоряет повторные вызовы."""
        n = 25

        # Очищаем кэш
        factorial_memoized.cache_clear()

        # Первый вызов (вычисление)
        time_first = measure_time(factorial_memoized, n, number=1)

        # Последующие вызовы (из кэша)
        time_cached = measure_time(factorial_memoized, n, number=100)
        avg_cached_time = time_cached / 100

        print(f"\nПервый вызов: {time_first:.8f} сек")
        print(f"Среднее время из кэша: {avg_cached_time:.10f} сек")

        # Проверяем, что время из кэша не больше первого вызова
        # (может быть немного больше из-за накладных расходов при очень малых значениях)
        assert avg_cached_time <= time_first * 1.5


# ============================================================
# Простые функции для быстрой проверки
# ============================================================

def test_simple():
    """Простейший тест для проверки работоспособности pytest."""
    assert factorial_iterative(5) == 120
    assert factorial_recursive(5) == 120
    print("✅ Простейший тест пройден!")


# ============================================================
# Запуск тестов при прямом выполнении файла
# ============================================================

if __name__ == "__main__":
    # Запуск всех тестов с подробным выводом
    pytest.main([__file__, "-v", "--tb=short", "--color=yes"])