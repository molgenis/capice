import os
import pickle
import unittest
import pandas as pd

from src.main_predict import Predict
from src.test.python.test_templates import set_up_manager_and_loc, teardown
from src.main.python.utilities.utilities import get_project_root_dir


class TestMainNonTrain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        manager, cls.output_dir = set_up_manager_and_loc()
        manager.output_filename = os.path.join(
            cls.output_dir,
            'test_output.txt'
        )
        with open(
                os.path.join(
                    get_project_root_dir(),
                    'CAPICE_model',
                    'GRCh37',
                    'POC',
                    'xgb_booster_poc.pickle.dat'
                ), 'rb'
        ) as model_file:
            cls.model = pickle.load(model_file)

    @classmethod
    def tearDownClass(cls):
        print('Performing teardown.')
        teardown()

    def setUp(self):
        print('Performing test:')

    def test_integration_main_nontrain(self):
        print('Main no-train (integration)')
        infile = os.path.join(get_project_root_dir(), 'CAPICE_example',
                              'CAPICE_input.tsv.gz')
        predict = Predict(input_loc=infile,
                          model=self.model,
                          output_loc=self.output_dir)
        predict.run()
        prediction_output = pd.read_csv(
            os.path.join(self.output_dir, 'test_output.txt'),
            compression='gzip',
            sep='\t'
        )
        self.assertEqual(prediction_output.shape, (20, 9))


if __name__ == '__main__':
    unittest.main()
