import os
import unittest

import pandas as pd

from molgenis.capice.main_predict import CapicePredict
from tests.capice.test_templates import set_up_manager_and_out, teardown, _project_root_directory, \
    ResourceFile, load_model


class TestMainNonTrain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        manager, cls.output_dir = set_up_manager_and_out()
        manager.output_filename = os.path.join(cls.output_dir, 'test_output.txt')

        cls.model = load_model(ResourceFile.XGB_BOOSTER_POC_UBJ.value)

    @classmethod
    def tearDownClass(cls):
        print('Performing teardown.')
        teardown()

    def setUp(self):
        print('Performing test:')

    def test_integration_main_nontrain(self):
        print('Main no-train (integration)')
        infile = os.path.join(_project_root_directory, 'resources', 'predict_input.tsv.gz')
        predict = CapicePredict(input_path=infile, model=self.model, output_path=self.output_dir,
                                output_given=True)
        predict.run()
        prediction_output = pd.read_csv(os.path.join(self.output_dir, 'test_output.txt'),
                                        compression='gzip',
                                        sep='\t')
        self.assertEqual(prediction_output.shape, (4, 11))


if __name__ == '__main__':
    unittest.main()
