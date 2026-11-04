"""Построение бинарного дерева с мемоизацией. Вариант 11."""

from collections import deque
from functools import lru_cache, wraps
from typing import Callable

Number = int | float
Tree = dict[str, object]
LeafFunc = Callable[[Number], Number]


def left11(x: Number) -> Number:
    """Вычислить левого потомка для варианта 11: root ^ 2."""
    return x ** 2


def right11(x: Number) -> Number:
    """Вычислить правого потомка для варианта 11: 2 + root ^ 2."""
    return 2 + x ** 2


def left13(x: Number) -> Number:
    """Вычислить левого потомка для варианта 13: x + 1."""
    return x + 1


def right13(x: Number) -> Number:
    """Вычислить правого потомка для варианта 13: x - 1."""
    return x - 1


def node(value: Number, left: Tree | None = None, right: Tree | None = None) -> Tree:
    """Создать словарь узла дерева."""
    return {"value": value, "left": left, "right": right}


def check_height(height: int) -> None:
    """Проверить корректность высоты дерева."""
    if type(height) is not int:
        raise TypeError("height должна быть целым числом")
    if height < 0:
        raise ValueError("height не может быть отрицательной")


def memoize(func: Callable) -> Callable:
    """Сохранить результаты вызовов по позиционным и именованным аргументам."""
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Именованные аргументы сортируются для постоянного порядка ключа.
        key = (args, tuple(sorted(kwargs.items())))
        if key in cache:
            wrapper.hits += 1
            return cache[key]
        wrapper.misses += 1
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    def cache_clear() -> None:
        """Очистить сохранённые результаты и обнулить счётчики."""
        cache.clear()
        wrapper.hits = 0
        wrapper.misses = 0

    def cache_info() -> dict[str, int]:
        """Вернуть число попаданий, промахов и записей в кэше."""
        return {"hits": wrapper.hits, "misses": wrapper.misses, "size": len(cache)}

    wrapper.hits = 0
    wrapper.misses = 0
    wrapper.cache_clear = cache_clear
    wrapper.cache_info = cache_info
    return wrapper


def gen_bin_tree_recursive(
    height: int = 3, root: Number = 11,
    left_leaf: LeafFunc = left11, right_leaf: LeafFunc = right11,
) -> Tree:
    """Рекурсивно построить дерево заданной высоты."""
    check_height(height)
    if height == 0:
        return node(root)
    return node(
        root,
        gen_bin_tree_recursive(height - 1, left_leaf(root), left_leaf, right_leaf),
        gen_bin_tree_recursive(height - 1, right_leaf(root), left_leaf, right_leaf),
    )


def gen_bin_tree_iterative(
    height: int = 3, root: Number = 11,
    left_leaf: LeafFunc = left11, right_leaf: LeafFunc = right11,
) -> Tree:
    """Построить дерево без рекурсии с помощью очереди (BFS)."""
    check_height(height)
    tree = node(root)
    queue = deque([(tree, 0)])
    while queue:
        current, depth = queue.popleft()
        if depth == height:
            continue
        value = current["value"]
        left = node(left_leaf(value))
        right = node(right_leaf(value))
        current["left"] = left
        current["right"] = right
        queue.append((left, depth + 1))
        queue.append((right, depth + 1))
    return tree


@memoize
def gen_bin_tree_recursive_memo(
    height: int = 3, root: Number = 11,
    left_leaf: LeafFunc = left11, right_leaf: LeafFunc = right11,
) -> Tree:
    """Рекурсивно построить дерево, используя кэш для поддеревьев."""
    check_height(height)
    if height == 0:
        return node(root)
    return node(
        root,
        gen_bin_tree_recursive_memo(height - 1, left_leaf(root), left_leaf, right_leaf),
        gen_bin_tree_recursive_memo(height - 1, right_leaf(root), left_leaf, right_leaf),
    )


def gen_bin_tree_iterative_memo(
    height: int = 3, root: Number = 11,
    left_leaf: LeafFunc = left11, right_leaf: LeafFunc = right11,
) -> Tree:
    """Построить дерево снизу вверх, сохраняя уникальные поддеревья."""
    check_height(height)
    levels = [{root}]
    children = {}

    # Собираем уникальные значения на каждом уровне.
    for depth in range(height):
        next_level = set()
        for value in levels[depth]:
            left, right = left_leaf(value), right_leaf(value)
            children[(height - depth, value)] = (left, right)
            next_level.update((left, right))
        levels.append(next_level)

    # Собираем словари снизу вверх, используя уже готовых потомков.
    cache = {}
    for depth in range(height, -1, -1):
        remaining = height - depth
        for value in levels[depth]:
            if remaining == 0:
                cache[(remaining, value)] = node(value)
            else:
                left, right = children[(remaining, value)]
                cache[(remaining, value)] = node(
                    value, cache[(remaining - 1, left)], cache[(remaining - 1, right)]
                )
    return cache[(height, root)]


@lru_cache(maxsize=None)
def gen_bin_tree_recursive_lru(
    height: int = 3, root: Number = 11,
    left_leaf: LeafFunc = left11, right_leaf: LeafFunc = right11,
) -> Tree:
    """Рекурсивно построить дерево с functools.lru_cache."""
    check_height(height)
    if height == 0:
        return node(root)
    return node(
        root,
        gen_bin_tree_recursive_lru(height - 1, left_leaf(root), left_leaf, right_leaf),
        gen_bin_tree_recursive_lru(height - 1, right_leaf(root), left_leaf, right_leaf),
    )