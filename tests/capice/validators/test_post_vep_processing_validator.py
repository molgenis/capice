import unittest

import pandas as pd

from tests.capice.test_templates import teardown, ResourceFile, load_model
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
        cls.validator = PostVEPProcessingValidator(
            load_model(ResourceFile.XGB_BOOSTER_POC_UBJ.value)
        )

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
