import os
import pickle
import unittest

import pandas as pd

from main.python.utilities.utilities import get_project_root_dir
from main.python.validators.post_vep_processing_validator import PostVEPProcessingValidator
from test.python.test_templates import teardown


class TestPostVEPProcessingValidator(unittest.TestCase):
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
        with open(
                os.path.join(
                    get_project_root_dir(),
                    'CAPICE_model',
                    'GRCh37',
                    'POC',
                    'xgb_booster_poc.pickle.dat'
                ), 'rb'
        ) as model_file:
            cls.validator = PostVEPProcessingValidator(pickle.load(model_file))

    @classmethod
    def tearDownClass(cls) -> None:
        print('Tearing down.')
        teardown()

    def test_validate_features_present_incorrect(self):
        print('KeyError raise due to missing VEP processed feature')
        self.assertRaises(
            KeyError,
            self.validator.validate_features_present,
            self.dataset
        )


if __name__ == '__main__':
    unittest.main()
