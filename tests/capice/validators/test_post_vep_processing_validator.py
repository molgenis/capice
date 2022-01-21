import os
import pickle
import unittest

import pandas as pd

from tests.capice.test_templates import teardown, _project_root_directory
from molgenis.capice.validators.post_vep_processing_validator import PostVEPProcessingValidator


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
                    _project_root_directory,
                    'tests',
                    'resources',
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
