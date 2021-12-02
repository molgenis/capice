import os
import shutil
import unittest
from pathlib import Path

import pandas as pd

from scripts.balance_dataset import correct_column_names, Split, Balancer, \
    CommandLineArgumentsValidator, InputDatasetValidator, __bins__
from src.main.python.utilities.utilities import get_project_root_dir


class TestBalancer(unittest.TestCase):
    __current_directory__ = get_project_root_dir()
    __test_path__ = os.path.join(__current_directory__, '.test_folder')

    @classmethod
    def setUpClass(cls) -> None:
        if not os.path.isdir(cls.__test_path__):
            os.makedirs(cls.__test_path__)
        cls.dataset = correct_column_names(
            pd.read_csv(
                os.path.join(
                    cls.__current_directory__,
                    'CAPICE_example',
                    'train_example.tsv.gz'
                ),
                sep='\t',
                na_values='.',
                low_memory=False
            )
        )

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.isdir(cls.__test_path__):
            for filename in os.listdir(cls.__test_path__):
                filepath = os.path.join(cls.__test_path__, filename)
                try:
                    if os.path.isfile(filepath) or os.path.islink(filepath):
                        os.unlink(filepath)
                    elif os.path.isdir(filepath):
                        shutil.rmtree(filepath)
                except Exception as e:
                    print(f'Failed to delete {filepath}, reason: {e}')
            try:
                os.rmdir(cls.__test_path__)
            except Exception as e:
                print(f'Failed to remove test folder {cls.__test_path__}, reason: {e}')

    def setUp(self) -> None:
        print('Testing Class:')

    def tearDown(self) -> None:
        print('Done.')

    def test_split(self):
        """
        Function to test the splitter class
        """
        print('Splitter')
        n_b_tot = self.dataset[self.dataset['binarized_label'] == 0].shape[0]
        p10_b = n_b_tot * 0.1
        p90_b = n_b_tot - p10_b
        n_p_tot = self.dataset[self.dataset['binarized_label'] == 1].shape[0]
        p10_p = n_p_tot * 0.1
        p90_p = n_p_tot - p10_p
        splitter = Split()
        copy_of_dataset = self.dataset.copy(deep=True)
        validation_dataset, dataset = splitter.split(copy_of_dataset)
        self.assertAlmostEqual(
            validation_dataset[validation_dataset['binarized_label'] == 0].shape[0], p10_b)
        self.assertAlmostEqual(
            validation_dataset[validation_dataset['binarized_label'] == 1].shape[0], p10_p)
        self.assertAlmostEqual(dataset[dataset['binarized_label'] == 0].shape[0], p90_b)
        self.assertAlmostEqual(dataset[dataset['binarized_label'] == 1].shape[0], p90_p)
        self.assertGreater(dataset.shape[0], 0)
        self.assertGreater(validation_dataset.shape[0], 0)

    def test_balancer(self):
        """
        Function to test the balancer
        """
        print('Balancer')
        balancer = Balancer()
        dataset = self.dataset.copy(deep=True)
        balanced_dataset = balancer.balance(dataset)
        self.assertGreater(balanced_dataset.shape[0], 0)
        self.assertEqual(
            balanced_dataset[balanced_dataset['binarized_label'] == 0].shape[0],
            balanced_dataset[balanced_dataset['binarized_label'] == 1].shape[0]
        )
        for ind in range(len(__bins__) - 1):
            lower_bound = __bins__[ind]
            upper_bound = __bins__[ind + 1]
            self.assertEqual(
                balanced_dataset[(balanced_dataset['MAX_AF'] >= lower_bound) &
                                 (balanced_dataset['MAX_AF'] < upper_bound) &
                                 (balanced_dataset['binarized_label'] == 0)].shape[0],
                balanced_dataset[(balanced_dataset['MAX_AF'] >= lower_bound) &
                                 (balanced_dataset['MAX_AF'] < upper_bound) &
                                 (balanced_dataset['binarized_label'] == 1)].shape[0]
            )

    def test_cla_validator(self):
        """
        Function to test the Command Line Arguments validator

        (does not test the -if directory is writable- validation, which is incredably difficult
        to implement)
        """
        print('CLA Validator')
        validator = CommandLineArgumentsValidator()
        self.assertRaises(
            FileNotFoundError,
            validator.validate_input_path,
            self.__current_directory__
        )
        self.assertRaises(
            FileNotFoundError,
            validator.validate_input_path,
            str(Path(__file__))
        )
        self.assertRaises(
            OSError,
            validator.validate_output_directory,
            os.path.join(self.__current_directory__, 'no', 'directory')
        )
        new_dir = '.another_test_output'
        validator.validate_output_directory(
            os.path.join(
                self.__current_directory__,
                new_dir
            )
        )
        self.assertIn(new_dir, os.listdir(self.__current_directory__))
        os.rmdir(os.path.join(self.__current_directory__, new_dir))

    def test_dataset_validator(self):
        """
        Function to test if the dataset validator does what it is supposed to.
        """
        print('Dataset validator')
        validator = InputDatasetValidator()
        dataset = self.dataset.copy(deep=True)
        self.assertRaises(KeyError,
                          validator.validate_columns_required,
                          dataset.drop(columns=['MAX_AF']))
        self.assertRaises(ValueError,
                          validator.validate_b_p_present,
                          dataset[dataset['binarized_label'] == 0])
        self.assertRaises(ValueError,
                          validator.validate_b_p_present,
                          dataset[dataset['binarized_label'] == 1])


if __name__ == '__main__':
    unittest.main()
