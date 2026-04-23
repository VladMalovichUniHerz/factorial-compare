"""Быстрая проверка работоспособности проекта."""


def quick_test():
    print("=" * 50)
    print("БЫСТРАЯ ПРОВЕРКА ПРОЕКТА")
    print("=" * 50)

    # 1. Проверка импортов
    print("\n1. Проверка импорта модулей...")
    try:
        from factorial_compare import (
            factorial_iterative, factorial_recursive,
            factorial_memoized, measure_time, compare_factorials, main
        )
        print("   ✅ Все функции импортированы успешно")
    except ImportError as e:
        print(f"   ❌ Ошибка импорта: {e}")
        return False

    # 2. Проверка вычислений
    print("\n2. Проверка корректности вычислений...")
    test_cases = [(0, 1), (5, 120), (7, 5040)]

    for n, expected in test_cases:
        iter_res = factorial_iterative(n)
        rec_res = factorial_recursive(n)
        factorial_memoized.cache_clear()
        mem_res = factorial_memoized(n)

        if iter_res == rec_res == mem_res == expected:
            print(f"   ✅ n={n}: все результаты верны ({expected})")
        else:
            print(f"   ❌ n={n}: ошибка в вычислениях")
            return False

    # 3. Проверка обработки ошибок
    print("\n3. Проверка обработки отрицательных чисел...")
    try:
        factorial_iterative(-1)
        print("   ❌ Итеративная: не вызвала ValueError")
        return False
    except ValueError:
        print("   ✅ Итеративная: корректно вызвала ValueError")

    try:
        factorial_recursive(-1)
        print("   ❌ Рекурсивная: не вызвала ValueError")
        return False
    except ValueError:
        print("   ✅ Рекурсивная: корректно вызвала ValueError")

    try:
        factorial_memoized(-1)
        print("   ❌ Мемоизированная: не вызвала ValueError")
        return False
    except ValueError:
        print("   ✅ Мемоизированная: корректно вызвала ValueError")

    # 4. Проверка функции замера времени
    print("\n4. Проверка функции measure_time...")
    try:
        result = measure_time(factorial_iterative, 10, number=10)
        if isinstance(result, float) and result > 0:
            print(f"   ✅ measure_time работает (время: {result:.8f} сек)")
        else:
            print("   ❌ measure_time вернула некорректное значение")
            return False
    except Exception as e:
        print(f"   ❌ Ошибка в measure_time: {e}")
        return False

    # 5. Проверка документации
    print("\n5. Проверка документации (PEP-257)...")
    functions = [factorial_iterative, factorial_recursive, factorial_memoized, measure_time]

    for func in functions:
        if func.__doc__ and len(func.__doc__.strip()) > 50:
            print(f"   ✅ {func.__name__}: документация присутствует")
        else:
            print(f"   ⚠️ {func.__name__}: документация отсутствует или слишком короткая")

    # 6. Проверка аннотаций типов
    print("\n6. Проверка аннотаций типов...")
    import inspect

    for func in functions:
        sig = inspect.signature(func)
        has_types = True

        for param in sig.parameters.values():
            if param.annotation == inspect.Parameter.empty:
                has_types = False
                break

        if sig.return_annotation == inspect.Signature.empty:
            has_types = False

        if has_types:
            print(f"   ✅ {func.__name__}: аннотации типов присутствуют")
        else:
            print(f"   ⚠️ {func.__name__}: отсутствуют некоторые аннотации")

    print("\n" + "=" * 50)
    print("✅ БЫСТРАЯ ПРОВЕРКА ПРОЙДЕНА УСПЕШНО!")
    print("=" * 50)

    # 7. Спросить о запуске основной программы
    print("\nЗапустить основную программу с графиком? (y/n): ", end="")
    response = input().strip().lower()

    if response == 'y':
        print("\nЗапуск основной программы...")
        print("(Закройте окно с графиком для завершения)\n")
        main()

    return True


if __name__ == "__main__":
    quick_test()