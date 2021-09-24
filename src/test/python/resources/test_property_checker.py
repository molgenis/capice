import unittest
from src.main.python.resources.checkers.property_checker import PropertyChecker


class TestPropertyChecker(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print('Setting up.')
        cls.property_checker = PropertyChecker()

    def setUp(self) -> None:
        print('Testing case:')

    def test_property_checker_correct(self):
        print('Property checker correct (not None)')
        value = 1.1
        expected_type = float
        self.property_checker.check_property(value, expected_type)

    def test_property_checker_correct_with_none(self):
        print('Property checker including None')
        value = None
        expected_type = float
        self.property_checker.check_property(
            value,
            expected_type,
            include_none=True
        )

    def test_property_checker_incorrect(self):
        print('Property checker incorrect (without none)')
        value = 1
        expected_type = float
        self.assertRaises(
            TypeError,
            self.property_checker.check_property,
            value,
            expected_type
        )

    def test_property_checker_incorrect_with_none(self):
        print('Property checker incorrect including None')
        value = None
        expected_type = float
        self.assertRaises(
            TypeError,
            self.property_checker.check_property,
            value,
            expected_type
        )


if __name__ == '__main__':
    unittest.main()
