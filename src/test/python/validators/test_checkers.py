import unittest
import pandas as pd

from src.main.python.validators.post_file_parse_validator import PostFileParseValidator
from src.test.python.test_templates import set_up_manager_and_out, teardown


class TestTrainValidator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        set_up_manager_and_out()
        cls.validator = PostFileParseValidator()

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        teardown()

    def setUp(self):
        print('Testing case:')

    def test_check_labels(self):
        print('Check labels')
        dataset = pd.DataFrame(columns=['chr', 'pos', 'ref', 'alt', 'binarized_label', 'foo'])
        self.assertRaises(
            KeyError,
            self.validator.validate_minimally_required_columns,
            dataset,
            ('binarized_label', 'sample_weight')
        )


if __name__ == '__main__':
    unittest.main()
