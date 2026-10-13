"""Модуль для генерации бинарного дерева."""

from typing import Callable

LEFT: Callable[[float], float] = lambda r: r ** 2
RIGHT: Callable[[float], float] = lambda r: 2 + r ** 2


def gen_bin_tree(
    height: int,
    root: float,
    left_leaf: Callable[[float], float] = LEFT,
    right_leaf: Callable[[float], float] = RIGHT,
) -> dict:
    """Рекурсивно строит бинарное дерево заданной высоты.

    Args:
        height: Высота дерева (количество уровней ниже корня).
        root: Значение в корне дерева.
        left_leaf: Функция вычисления значения левого потомка.
        right_leaf: Функция вычисления значения правого потомка.

    Returns:
        Словарь с ключами 'value', 'left', 'right'. При height = 0
        потомки равны None.
    """
    node: dict = {"value": root, "left": None, "right": None}

    if height:
        node["left"] = gen_bin_tree(height - 1, left_leaf(root), left_leaf, right_leaf)
        node["right"] = gen_bin_tree(height - 1, right_leaf(root), left_leaf, right_leaf)

    return node


if __name__ == "__main__":
    print(gen_bin_tree(3, 11))