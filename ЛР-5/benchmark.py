"""Сравнение времени построения деревьев. Запуск: python benchmark.py."""
from pathlib import Path
from timeit import Timer
from statistics import mean
import matplotlib.pyplot as plt

from app import (
    left11, right11, left13, right13, gen_bin_tree_recursive,
    gen_bin_tree_iterative, gen_bin_tree_recursive_memo,
    gen_bin_tree_iterative_memo, gen_bin_tree_recursive_lru,
)

HEIGHTS = range(2, 11)  # Для варианта 11 берем до 10
REPEATS = 7
FUNCTIONS = {
    "Рекурсивная": gen_bin_tree_recursive,
    "Итеративная": gen_bin_tree_iterative,
    "Свой memoize": gen_bin_tree_recursive_memo,
    "Итеративная с кэшем": gen_bin_tree_iterative_memo,
    "lru_cache": gen_bin_tree_recursive_lru,
}
VARIANTS = {11: (11, left11, right11), 13: (13, left13, right13)}


def clear_cache() -> None:
    """Очистить кэши рекурсивных функций."""
    gen_bin_tree_recursive_memo.cache_clear()
    gen_bin_tree_recursive_lru.cache_clear()


def measure(func, args, repeated: bool = False) -> float:
    """Вернуть среднее время одного вызова в миллисекундах."""
    def setup():
        clear_cache()
        if repeated:
            func(*args)  # Первый вызов заполняет кэш.

    timer = Timer(lambda: func(*args), setup=setup)
    return mean(timer.repeat(repeat=REPEATS, number=1)) * 1000


def count_calls(func, args) -> tuple[int, int]:
    """Посчитать вызовы функций левого и правого потомка."""
    height, root, left, right = args
    calls = [0, 0]

    def count_left(x):
        calls[0] += 1
        return left(x)

    def count_right(x):
        calls[1] += 1
        return right(x)

    clear_cache()
    func(height, root, count_left, count_right)
    return calls[0], calls[1]


def plot(variant: int, results: dict, label: str) -> None:
    """Построить и сохранить график сравнения функций."""
    plt.figure(figsize=(9, 5))
    for name, times in results.items():
        plt.plot(list(HEIGHTS), times, marker="o", label=name)
    plt.title(f"Вариант {variant}: {label}")
    plt.xlabel("Высота дерева")
    plt.ylabel("Время, мс")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    kind = "first" if label == "одно построение" else "repeat"
    plt.savefig(Path(__file__).parent / f"variant_{variant}_{kind}.png")
    plt.close()


def main() -> None:
    """Измерить скорость, вывести таблицы и сохранить четыре графика."""
    for variant, params in VARIANTS.items():
        root, left, right = params
        first = {name: [] for name in FUNCTIONS}
        repeat = {name: [] for name in ("Свой memoize", "lru_cache")}

        print(f"\nВариант {variant}. Одно построение (мс):")
        print("Высота | " + " | ".join(FUNCTIONS))
        for height in HEIGHTS:
            args = (height, root, left, right)
            for name, func in FUNCTIONS.items():
                first[name].append(measure(func, args))
            for name in repeat:
                repeat[name].append(measure(FUNCTIONS[name], args, repeated=True))
            print(f"{height:>6} | " + " | ".join(
                f"{first[name][-1]:.4f}" for name in FUNCTIONS))

        print("\nПовторный вызов (мс):")
        print("Высота | Свой memoize | lru_cache")
        for i, height in enumerate(HEIGHTS):
            print(f"{height:>6} | {repeat['Свой memoize'][i]:.6f} | "
                  f"{repeat['lru_cache'][i]:.6f}")

        args = (9, root, left, right)
        print("\nЧисло вызовов left_leaf/right_leaf при height=9:")
        for name, func in FUNCTIONS.items():
            l, r = count_calls(func, args)
            print(f"{name}: {l} / {r}")

        plot(variant, first, "одно построение")
        plot(variant, repeat, "повторный вызов")

    clear_cache()
    gen_bin_tree_recursive_lru(9, 13, left13, right13)
    print("\nlru_cache.cache_info():", gen_bin_tree_recursive_lru.cache_info())
    clear_cache()


if __name__ == "__main__":
    main()