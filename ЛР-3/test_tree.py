"""Тесты для модуля генерации бинарного дерева."""

import unittest

from tree import gen_bin_tree


class TestGenBinTree(unittest.TestCase):
    """Набор тестов для функции gen_bin_tree (вариант: root=11, height=3)."""

    def test_root_value(self) -> None:
        """Проверяет, что корень дерева содержит переданное значение."""
        tree: dict = gen_bin_tree(3, 11)
        self.assertEqual(tree["value"], 11)

    def test_left_right(self) -> None:
        """Проверяет значения левого и правого потомков при height=1."""
        tree: dict = gen_bin_tree(1, 11)
        self.assertEqual(tree["left"]["value"], 121)
        self.assertEqual(tree["right"]["value"], 123)

    def test_height_zero(self) -> None:
        """Проверяет, что при height=0 узел является листом без потомков."""
        tree: dict = gen_bin_tree(0, 11)
        self.assertEqual(tree, {"value": 11, "left": None, "right": None})


if __name__ == "__main__":
    unittest.main(argv=[""], verbosity=2, exit=False)