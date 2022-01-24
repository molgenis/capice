import os
import pickle
import unittest

import pandas as pd

from molgenis.capice.main_predict import CapicePredict
from tests.capice.test_templates import set_up_manager_and_out, teardown, _project_root_directory


class TestMainNonTrain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        manager, cls.output_dir = set_up_manager_and_out()
        manager.output_filename = os.path.join(cls.output_dir, 'test_output.txt')
        with open(
                os.path.join(
                    _project_root_directory,
                    'tests',
                    'resources',
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
        infile = os.path.join(_project_root_directory, 'CAPICE_example', 'CAPICE_input.tsv.gz')
        predict = CapicePredict(input_path=infile, model=self.model, output_path=self.output_dir)
        predict.run()
        prediction_output = pd.read_csv(os.path.join(self.output_dir, 'test_output.txt'),
                                        compression='gzip',
                                        sep='\t')
        self.assertEqual(prediction_output.shape, (7, 10))


if __name__ == '__main__':
    unittest.main()
