import unittest

import pytest

from src.main.python.resources.utilities.utilities import \
    validate_list_length_one
from src.main.python.resources.utilities import utilities


class TestUtilities(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up')
        cls.utils = utilities

    def setUp(self):
        print('Testing case:')

    def test_validate_list_length_one_valid_list(self):
        input_list = ['aa']
        expected_output = 'aa'
        actual_output = validate_list_length_one(input_list)

        assert actual_output == expected_output

    def test_validate_list_length_one_none(self):
        input_list = None
        expected_output = None
        actual_output = validate_list_length_one(input_list)

        assert actual_output == expected_output

    def test_validate_list_length_one_emtpy(self):
        input_list = []

        with pytest.raises(ValueError) as err:
            validate_list_length_one(input_list)

        msg = 'Empty list is given. Should be None or list with elements.'
        assert str(err.value) == msg

    def test_validate_list_length_one_too_long(self):
        input_list = ['aa', 'bb']

        with pytest.raises(ValueError) as err:
            validate_list_length_one(input_list)

        msg = 'List contains more than 1 item.'
        assert str(err.value) == msg


if __name__ == '__main__':
    unittest.main()
