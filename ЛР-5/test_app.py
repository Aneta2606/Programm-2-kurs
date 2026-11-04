"""Тесты для пяти способов построения бинарного дерева (Вариант 11)."""

import unittest
from app import (
    memoize, left13, right13, gen_bin_tree_recursive,
    gen_bin_tree_iterative, gen_bin_tree_recursive_memo,
    gen_bin_tree_iterative_memo, gen_bin_tree_recursive_lru,
)


class TreeTests(unittest.TestCase):
    """Проверить равенство деревьев и работу кэша."""

    def setUp(self) -> None:
        """Очистить кэши перед тестом."""
        gen_bin_tree_recursive_memo.cache_clear()
        gen_bin_tree_recursive_lru.cache_clear()

    def test_equal_trees(self) -> None:
        """Все функции должны строить одинаковое дерево."""
        functions = (gen_bin_tree_iterative, gen_bin_tree_recursive_memo,
                     gen_bin_tree_iterative_memo, gen_bin_tree_recursive_lru)
        # Проверяем значения по умолчанию (Вариант 11) и кастомные (Вариант 13)
        for args in ((), (4, 13, left13, right13), (0, 11)):
            expected = gen_bin_tree_recursive(*args)
            for func in functions:
                self.assertEqual(func(*args), expected)

    def test_memoize(self) -> None:
        """Декоратор должен запоминать результаты и очищать кэш."""
        calls = []

        @memoize
        def add(a: int, b: int) -> int:
            """Сложить числа."""
            calls.append(1)
            return a + b

        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(a=2, b=4), 6)
        self.assertEqual(add(b=4, a=2), 6)
        self.assertEqual(len(calls), 2)
        self.assertEqual(add.hits, 2)
        self.assertEqual(add.misses, 2)
        self.assertEqual(add.__name__, "add")
        self.assertEqual(add.__doc__, "Сложить числа.")
        add.cache_clear()
        self.assertEqual((add.hits, add.misses), (0, 0))

    def test_shared_nodes(self) -> None:
        """Мемоизованные деревья содержат общие объекты-поддеревья."""
        args = (2, 13, left13, right13)
        for func in (gen_bin_tree_recursive_memo,
                     gen_bin_tree_iterative_memo, gen_bin_tree_recursive_lru):
            tree = func(*args)
            self.assertIs(tree["left"]["right"], tree["right"]["left"])
            tree["left"]["right"]["value"] = 100
            self.assertEqual(tree["right"]["left"]["value"], 100)
            if func is not gen_bin_tree_iterative_memo:
                self.assertEqual(func(*args)["right"]["left"]["value"], 100)
                func.cache_clear()
        plain = gen_bin_tree_recursive(*args)
        self.assertIsNot(plain["left"]["right"], plain["right"]["left"])

    def test_invalid_height(self) -> None:
        """Отрицательная и дробная высоты недопустимы."""
        for func in (gen_bin_tree_recursive, gen_bin_tree_iterative,
                     gen_bin_tree_recursive_memo, gen_bin_tree_iterative_memo,
                     gen_bin_tree_recursive_lru):
            with self.assertRaises(ValueError):
                func(-1)
            with self.assertRaises(TypeError):
                func(1.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)