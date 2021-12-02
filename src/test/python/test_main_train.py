import os
import pickle
import unittest

from src.main.python.utilities.utilities import get_project_root_dir
from src.main_train import CapiceTrain
from src.test.python.test_templates import set_up_manager_and_out, teardown


class TestMainTrain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        manager, cls.output_dir = set_up_manager_and_out()
        cls.output_filename = 'train_example_capice.pickle.dat'
        manager.output_filename = cls.output_filename
        train_file = os.path.join(get_project_root_dir(), 'CAPICE_example', 'train_example.tsv.gz')
        impute_json = os.path.join(get_project_root_dir(),
                                   'CAPICE_example',
                                   'example_impute_values.json')
        cls.main = CapiceTrain(input_path=train_file,
                               json_path=impute_json,
                               test_split=0.2,
                               output_path=cls.output_dir)
        cls.main.esr = 1
        cls.main.n_jobs = 2
        cls.main.cross_validate = 2
        cls.main.n_iterations = 2

    @classmethod
    def tearDownClass(cls):
        print('Performing teardown.')
        teardown()

    def tearDown(self):
        print('Resetting arguments.')

    def setUp(self):
        print('Performing test:')

    def test_integration_training(self):
        """
        Integration test for the full training part of CAPICE.
        With check if the correct class is exported.
        """
        print('Training (integration)')
        self.main.run()
        output_path = os.path.join(self.output_dir, self.output_filename)
        with open(output_path, 'rb') as model_dat:
            model = pickle.load(model_dat)
        best_model = str(model.__class__).split("'")[1]
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
        self.assertAlmostEqual(train.shape[0], total_size * 0.8)
        self.assertAlmostEqual(test.shape[0], total_size * 0.2)
        self.assertEqual(train.shape[0] + test.shape[0], total_size)


if __name__ == '__main__':
    unittest.main()
