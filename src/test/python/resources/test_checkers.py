import unittest
import pandas as pd
from src.main.python.resources.errors.errors import InputError
from src.main.python.resources.checkers.train_checker import TrainChecker
from src.main.python.resources.checkers.property_checker import PropertyChecker
from src.main.python.resources.checkers.property_checker_logger import PropertyCheckerLogger
from src.main.python.resources.checkers.cadd_version_checker import CaddVersionChecker
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
        dataset = pd.DataFrame(columns=['binarized_label', 'sample_weight', 'foo', 'max_AF'])
        with self.assertRaises(KeyError):
            self.train_checker.check_labels(dataset=dataset, include_balancing=True)


class TestCaddVersionChecker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up')
        cls.manager, output = set_up_manager_and_loc()
        cls.cadd_build = False
        cls.grch_build = False

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        teardown()

    def setUp(self):
        print('Testing case:')

    def test_raise_overrule_error(self):
        print('Overrule error')
        with self.assertRaises(InputError):
            CaddVersionChecker(
                cla_cadd_version=False,
                cla_grch_build=False,
                file_cadd_version=False,
                file_grch_build=False
            )

    def test_file_cla_mismatch_cadd(self):
        print('File and Config CADD versions mismatch')
        config_cadd_version = 1.4
        file_cadd_version = 1.6
        config_grch_version = 37
        file_grch_version = 37
        with self.assertWarns(Warning):
            CaddVersionChecker(
                cla_cadd_version=config_cadd_version,
                cla_grch_build=config_grch_version,
                file_cadd_version=file_cadd_version,
                file_grch_build=file_grch_version
            )

    def test_file_cla_mismatch_grch(self):
        print('File and Config GRCh builds mismatch')
        config_cadd_version = 1.4
        file_cadd_version = 1.4
        config_grch_version = 38
        file_grch_version = 37
        with self.assertWarns(Warning):
            CaddVersionChecker(
                cla_cadd_version=config_cadd_version,
                cla_grch_build=config_grch_version,
                file_cadd_version=file_cadd_version,
                file_grch_build=file_grch_version
            )


class TestPropertyCheckers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up')
        set_up_manager_and_loc()
        cls.property_checker = PropertyChecker()
        cls.property_checker_log = PropertyCheckerLogger()
        cls.variable = 1.1
        cls.incorrect_variable_type = str

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        teardown()

    def setUp(self):
        print('Testing case:')

    def test_property_checker_raise(self):
        print('Raise property mismatch no log')
        with self.assertRaises(TypeError):
            self.property_checker.check_property(value=self.variable,
                                                 expected_type=self.incorrect_variable_type,
                                                 include_none=True)

    def test_property_checker_raise_log(self):
        print('Raise property mismatch with log')
        with self.assertRaises(TypeError):
            self.property_checker_log.check_property(value=self.variable,
                                                     expected_type=self.incorrect_variable_type,
                                                     include_none=True)


if __name__ == '__main__':
    unittest.main()
