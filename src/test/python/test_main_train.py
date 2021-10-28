import unittest
import os
import pickle
from src.main_train import Train
from src.test.python.test_templates import set_up_manager_and_loc, teardown
from src.main.python.resources.utilities.utilities import get_project_root_dir


__program__ = 'Main Train test'
__version__ = 'testing'
__author__ = 'R.J. Sietsma'


class TestMainTrain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.manager, cls.output_dir = set_up_manager_and_loc()
        train_file = os.path.join(get_project_root_dir(),
                                  'CAPICE_example',
                                  'train_dataset.tsv.gz'
                                  )
        cls.main = Train(input_loc=train_file,
                         json_loc=None,
                         test_split=0.2,
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
        input_file = self.main._load_file()
        self.main.split_data(dataset=input_file, test_size=0.2)

    def test_component_split(self):
        """
        Component test for split to see if the correct sizes of datasets are
        created.
        """
        print('Split (component)')
        input_file = self.main._load_file()
        train, test = self.main.split_data(dataset=input_file, test_size=0.2)
        total_size = input_file.shape[0]
        self.assertAlmostEqual(train.shape[0], total_size*0.8)
        self.assertAlmostEqual(test.shape[0], total_size*0.2)
        self.assertEqual(train.shape[0] + test.shape[0], total_size)


if __name__ == '__main__':
    unittest.main()
