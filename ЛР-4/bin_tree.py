"""Модуль для нерекурсивной генерации бинарного дерева."""

from collections import deque
from typing import Any, Callable

DEFAULT_LEFT: Callable[[int], int] = lambda r: r ** 2
DEFAULT_RIGHT: Callable[[int], int] = lambda r: 2 + r ** 2


def gen_bin_tree(
    height: int = 3,
    root: int = 11,
    left_leaf: Callable[[int], int] = DEFAULT_LEFT,
    right_leaf: Callable[[int], int] = DEFAULT_RIGHT,
) -> dict[str, Any]:
    """Строит бинарное дерево заданной высоты нерекурсивно (BFS).

    Args:
        height: Высота дерева (количество уровней ниже корня).
        root: Значение в корне дерева.
        left_leaf: Функция вычисления значения левого потомка.
        right_leaf: Функция вычисления значения правого потомка.

    Returns:
        Корень дерева в виде словаря с ключами 'value', 'left', 'right'.
        Листья имеют left = right = None.

    Raises:
        ValueError: Если height < 0.
    """
    if height < 0:
        raise ValueError("Высота не может быть отрицательной")

    root_node: dict[str, Any] = {"value": root, "left": None, "right": None}
    queue = deque([(root_node, height)])

    while queue:
        node, current_height = queue.popleft()

        if current_height == 0:
            continue

        left_child = {"value": left_leaf(node["value"]), "left": None, "right": None}
        right_child = {"value": right_leaf(node["value"]), "left": None, "right": None}

        node["left"] = left_child
        node["right"] = right_child

        queue.append((left_child, current_height - 1))
        queue.append((right_child, current_height - 1))

    return root_node


if __name__ == "__main__":
    from pprint import pprint
    pprint(gen_bin_tree())