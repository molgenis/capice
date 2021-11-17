import unittest

from src.main.python.utilities.utilities import \
    validate_list_length_one


class TestUtilities(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up')

    def setUp(self):
        print('Testing case:')

    def test_validate_list_length_one_valid_list(self):
        input_list = ['aa']
        expected_output = 'aa'
        actual_output = validate_list_length_one(input_list)
        self.assertEqual(actual_output, expected_output)

    def test_validate_list_length_one_none(self):
        input_list = None
        expected_output = None
        actual_output = validate_list_length_one(input_list)
        self.assertEqual(actual_output, expected_output)

    def test_validate_list_length_one_emtpy(self):
        input_list = []
        with self.assertRaises(ValueError) as context:
            validate_list_length_one(input_list)
        msg = 'Empty list is given. Should be None or list with elements.'
        self.assertEqual(str(context.exception), msg)

    def test_validate_list_length_one_too_long(self):
        input_list = ['aa', 'bb']
        with self.assertRaises(ValueError) as context:
            validate_list_length_one(input_list)
        msg = 'List contains more than 1 item.'
        self.assertEqual(str(context.exception), msg)


if __name__ == '__main__':
    unittest.main()
