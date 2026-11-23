import unittest
from add import add


class TestAddFunction(unittest.TestCase):

    def test_basic_scenario(self):
        """1. Базовый случай: пара находится в середине списка."""
        nums = [3, 2, 4, 15]
        target = 6
        self.assertIn(add(nums, target), ([1, 2], [2, 1]))

    def test_pair_at_boundaries(self):
        """2. Пара находится в начале и в самом конце списка."""
        nums = [10, 5, 8, 20]
        target = 30
        self.assertIn(add(nums, target), ([0, 3], [3, 0]))

    def test_no_solution(self):
        """3. Пары нет, функция должна вернуть None."""
        nums = [1, 2, 3, 4]
        target = 100
        self.assertIsNone(add(nums, target))

    def test_empty_list(self):
        """4. Крайний случай: пустой список."""
        self.assertIsNone(add([], 5))

    def test_one_element_list(self):
        """5. Крайний случай: список из одного элемента."""
        self.assertIsNone(add([5], 10))

    def test_same_elements_not_reused(self):
        """6. Один и тот же элемент не используется дважды."""
        nums = [3, 4, 5]
        target = 6
        self.assertIsNone(add(nums, target))

    def test_negative_numbers(self):
        """7. Работа с отрицательными числами."""
        nums = [-10, 5, -2, 8]
        target = -12
        self.assertIn(add(nums, target), ([0, 2], [2, 0]))

    def test_zeros_and_duplicates(self):
        """8. Работа с нулями и дубликатами."""
        nums = [0, 0, 4, 5]
        target = 0
        self.assertIn(add(nums, target), ([0, 1], [1, 0]))

    def test_original_list_unchanged(self):
        """9. Функция не изменяет исходный список."""
        nums = [1, 2, 3]
        target = 4
        original_copy = nums.copy()
        add(nums, target)
        self.assertEqual(
            nums, original_copy, "Функция не должна изменять исходный список"
        )


if __name__ == "__main__":
    unittest.main()
