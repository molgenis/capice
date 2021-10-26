import unittest
import pandas as pd
from src.main.python.resources.errors.errors import InputError
from src.main.python.resources.checkers.train_checker import TrainChecker
from src.test.python.test_templates import set_up_manager_and_loc, teardown


class TestTrainChecker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        set_up_manager_and_loc()
        cls.train_checker = TrainChecker()

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        teardown()

    def setUp(self):
        print('Testing case:')

    def test_check_specified_defaults_nokey(self):
        print('Check specified defaults (key not found)')
        json = {
            'learning_rate': 0.1,
            'n_estimators': 10
        }
        with self.assertRaises(KeyError):
            self.train_checker.check_specified_defaults(loaded_defaults=json)

    def test_check_specified_defaults_wrong_type(self):
        print('Check specified defaults (incorrect variable type)')
        json = {
            'learning_rate': 0.1,
            'n_estimators': 10,
            'max_depth': 'foo'
        }
        with self.assertRaises(TypeError):
            self.train_checker.check_specified_defaults(loaded_defaults=json)

    def test_check_labels(self):
        print('Check labels')
        dataset = pd.DataFrame(columns=['binarized_label', 'sample_weight',
                                        'foo', 'max_AF'])
        with self.assertRaises(KeyError):
            self.train_checker.check_labels(
                dataset=dataset
            )


if __name__ == '__main__':
    unittest.main()
