import unittest
import os
import pickle
from src.main_train import Train
from src.test.python.test_templates import set_up_manager_and_loc, teardown
from src.main.python.core.config_reader import ConfigReader
from src.main.python.resources.utilities.utilities import get_project_root_dir


__program__ = 'Main Train test'
__version__ = 'testing'
__author__ = 'R.J. Sietsma'


class TestMainTrain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.manager, cls.output_dir = set_up_manager_and_loc()
        cls.manager.overwrite_impute = 'VEP104'
        train_file = os.path.join(get_project_root_dir(),
                                  'CAPICE_example',
                                  'train_dataset.tsv.gz'
                                  )
        ConfigReader().parse()
        cls.main = Train(__program__=__program__,
                         __author__=__author__,
                         __version__=__version__,
                         input_loc=train_file,
                         output_loc=cls.output_dir)

    @classmethod
    def tearDownClass(cls):
        print('Performing teardown.')
        teardown()

    def tearDown(self):
        print('Resetting arguments.')
        self.main.default = False
        self.main.balance = False
        self.main.specified_default = False
        self.main._integration_test = False

    def setUp(self):
        print('Performing test:')

    def test_integration_training(self):
        """
        Integration test for the full training part of CAPICE.
        With check if the correct class is exported.
        """
        print('Training (integration)')
        self.main._integration_test = True
        self.main.run()
        output_filename = "randomized_search_cv_" + \
                          self.manager.now.strftime("%H%M%S%f_%d%m%Y") + \
                          '.pickle.dat'
        output_loc = os.path.join(self.output_dir, output_filename)
        with open(output_loc, 'rb') as model_dat:
            model = pickle.load(model_dat)
        class_used = str(model.__class__).split("'")[1]
        self.assertEqual(
            'sklearn.model_selection._search.RandomizedSearchCV', class_used)
        best_model = str(model.best_estimator_.__class__).split("'")[1]
        self.assertEqual('xgboost.sklearn.XGBClassifier', best_model)

    def test_unit_split(self):
        """
        Unit test to see if split works.
        """
        print('Split (unit)')
        input_file = self.main.load_file()
        self.main.split_data(dataset=input_file, test_size=0.2)

    def test_component_split(self):
        """
        Component test for split to see if the correct sizes of datasets are
        created.
        """
        print('Split (component)')
        input_file = self.main.load_file()
        train, test = self.main.split_data(dataset=input_file, test_size=0.2)
        total_size = input_file.shape[0]
        self.assertAlmostEqual(train.shape[0], total_size*0.8)
        self.assertAlmostEqual(test.shape[0], total_size*0.2)
        self.assertEqual(train.shape[0] + test.shape[0], total_size)

    def test_unit_load_defaults(self):
        """
        Unit test to see if the default hyper parameters can be loaded.
        """
        print('Load_defaults (unit)')
        self.main.load_defaults()

    def test_unit_load_specified_defaults(self):
        """
        Unit test to see if specified default hyper parameters can be loaded.
        """
        print('Load_specified_defaults (unit)')
        self.main.specified_default = os.path.join(
            get_project_root_dir(),
            'CAPICE_example',
            'specified_defaults.json'
        )
        self.main.load_defaults()

    def test_component_load_defaults(self):
        """
        Component test to see if default hyper parameters are correctly loaded
        according to expectation.
        """
        print('Load_defaults (component)')
        self.main.load_defaults()
        defaults = self.main.defaults
        self.assertEqual(defaults['learning_rate'], 0.10495845238185281)
        self.assertEqual(defaults['max_depth'], 422)
        self.assertEqual(defaults['n_estimators'], 15)

    def test_component_load_specified_defaults(self):
        """
        Component test to see if specified default hyper parameters are loaded
        correctly.
        """
        print('Load_specified_defaults (component)')
        self.main.specified_default = os.path.join(
            get_project_root_dir(),
            'CAPICE_example',
            'specified_defaults.json'
        )
        self.main.load_defaults()
        defaults = self.main.defaults
        self.assertEqual(defaults['learning_rate'], 0.5)
        self.assertEqual(defaults['max_depth'], 10)
        self.assertEqual(defaults['n_estimators'], 10)

    def test_unit_balancing(self):
        """
        Unit test for the balancing algorithm.
        """
        print('Balancing (unit)')
        self.main.process_balance_in_the_force(dataset=self.main.load_file())

    def test_component_balancing(self):
        """
        Component test for the balancing with test to see if the amount of
        benign and pathogenic variants are the same.
        """
        print('Balancing (component)')
        balanced_file = self.main.process_balance_in_the_force(
            dataset=self.main.load_file()
        )
        n_zero = balanced_file[balanced_file['binarized_label'] == 0].shape[0]
        n_one = balanced_file[balanced_file['binarized_label'] == 1].shape[0]
        self.assertEqual(n_zero, n_one)


if __name__ == '__main__':
    unittest.main()
