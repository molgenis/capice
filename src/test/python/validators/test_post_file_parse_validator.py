import unittest
import pandas as pd

from src.test.python.test_templates import teardown
from src.main.python.validators.post_file_parse_validator import PostFileParseValidator


class TestPostFileParseValidator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print('Setting up.')
        cls.dataset = pd.DataFrame(
            {
                'chr': [1, 2],
                'pos': [100, 200],
                'ref': ['A', 'A'],
                'alt': ['T', 'T'],
                'feat1': ['foo', 'bar']
            }
        )
        cls.validator = PostFileParseValidator()

    @classmethod
    def tearDownClass(cls) -> None:
        print('Tearing down.')
        teardown()

    def test_validation_correct_n_columns(self):
        print('Correct validation n_columns')
        self.validator.validate_n_columns(self.dataset)

    def test_validation_incorrect_n_columns(self):
        print('KeyError raised in n_columns due to too few columns (incorrectly loaded)')
        incorrectly_loaded_dataset = self.dataset[self.dataset.columns].astype(str).agg(
            '_'.join, axis=1
        )
        self.assertRaises(
            KeyError,
            self.validator.validate_n_columns,
            incorrectly_loaded_dataset
        )

    def test_validation_correct_required_columns(self):
        print('Correct validation required_columns')
        self.validator.validate_minimally_required_columns(
            self.dataset,
            additional_required_features=['feat1']
        )

    def test_validation_incorrect_required_columns_preset_required(self):
        print('KeyError raised due to missing ref column')
        self.assertRaises(
            KeyError,
            self.validator.validate_minimally_required_columns,
            self.dataset.drop(columns='ref'),
            additional_required_features='feat1'
        )

    def test_validation_incorrect_required_columns(self):
        print('KeyError raised due to missing feat2 column')
        self.assertRaises(
            KeyError,
            self.validator.validate_minimally_required_columns,
            self.dataset,
            additional_required_features=('feat1', 'feat2')
        )

    def test_validation_correct_chrom_pos(self):
        print('Correct validation chrom_pos not empty')
        self.validator.validate_chrom_pos(self.dataset)

    def test_validation_incorrect_chrom_pos(self):
        print('ValueError raised due to gap in pos column')
        incorrect_dataset = self.dataset.copy(deep=True)
        incorrect_dataset.iloc[1, 1] = None
        self.assertRaises(
            ValueError,
            self.validator.validate_chrom_pos,
            incorrect_dataset
        )


if __name__ == '__main__':
    unittest.main()
