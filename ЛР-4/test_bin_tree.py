"""Тесты для нерекурсивной генерации бинарного дерева."""

import unittest
from bin_tree import gen_bin_tree


class TestGenBinTree(unittest.TestCase):
    """Тесты для функции gen_bin_tree (вариант: root=11, height=3)."""

    def test_first_level_defaults(self) -> None:
        """Проверяет лист и потомков первого уровня по умолчанию."""
        t_leaf = gen_bin_tree(0, 11)
        self.assertEqual(t_leaf["value"], 11)
        self.assertIsNone(t_leaf["left"])

        t = gen_bin_tree(1, 11)
        self.assertEqual(t["left"]["value"], 121)
        self.assertEqual(t["right"]["value"], 123)

    def test_default_arguments(self) -> None:
        """Проверяет, что без аргументов используются значения варианта."""
        t = gen_bin_tree()
        self.assertEqual(t["value"], 11)
        self.assertEqual(t["left"]["value"], 121)
        self.assertEqual(t["right"]["value"], 123)

    def test_custom_functions(self) -> None:
        """Проверяет работу с пользовательскими функциями."""
        t = gen_bin_tree(1, 5, lambda x: x + 10, lambda x: x * 2)
        self.assertEqual(t["left"]["value"], 15)
        self.assertEqual(t["right"]["value"], 10)

    def test_negative_height(self) -> None:
        """При отрицательной высоте выбрасывается ValueError."""
        with self.assertRaises(ValueError):
            gen_bin_tree(-1, 11)


if __name__ == "__main__":
    unittest.main(verbosity=2)