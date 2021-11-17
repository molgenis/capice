import unittest

from src.main.python.validators.property_type_validator import \
    PropertyTypeValidator


class TestPropertyTypeValidator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print('Setting up.')
        cls.property_validator = PropertyTypeValidator()

    def setUp(self) -> None:
        print('Testing case:')

    def test_property_validator_correct(self):
        print('Property validator correct (not None)')
        value = 1.1
        expected_type = float
        self.property_validator.validate_property(value, expected_type)

    def test_property_validator_correct_with_none(self):
        print('Property validator including None')
        value = None
        expected_type = float
        self.property_validator.validate_property(
            value,
            expected_type,
            include_none=True
        )

    def test_property_validator_incorrect(self):
        print('Property validator incorrect (without none)')
        value = 1
        expected_type = float
        self.assertRaises(
            TypeError,
            self.property_validator.validate_property,
            value,
            expected_type
        )

    def test_property_validator_incorrect_with_none(self):
        print('Property validator incorrect including None')
        value = None
        expected_type = float
        self.assertRaises(
            TypeError,
            self.property_validator.validate_property,
            value,
            expected_type
        )

    def test_property_validator_int_bool(self):
        print('Property validator with expected int and value is False')
        value = False
        expected_type = int
        self.assertRaises(
            TypeError,
            self.property_validator.validate_property,
            value,
            expected_type
        )

    def test_property_validator_int_bool_include_none(self):
        print('Property validator with expected int, value is False and '
              'include_none is True')
        value = False
        expected_type = int
        self.assertRaises(
            TypeError,
            self.property_validator.validate_property,
            value,
            expected_type,
            True
        )


if __name__ == '__main__':
    unittest.main()
