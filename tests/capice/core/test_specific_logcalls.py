import os
import pickle
import unittest
import pandas as pd

from molgenis.capice.core.capice_manager import CapiceManager
from molgenis.capice.utilities.capice_imputing import CapiceImputing
from tests.capice.test_templates import teardown, _project_root_directory


class TestSpecificLogCalls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.manager = CapiceManager()
        cls.manager.loglevel = 10
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
        print('Tearing down.')
        teardown()

    def setUp(self):
        print('Testing case:')

    def test_nan_calculator(self):
        print('Nan calculator (using piping of stderr to variable)')
        nan_dataframe = pd.DataFrame(
            {
                'foo': [1, 2, 3, 4],
                'bar': [55, None, None, 66],
                'baz': [None, 77, 88, 99]
            }
        )
        messages_present = [
            'DEBUG:CAPICE:NaN detected in column bar, percentage: 50.0%.',
            'DEBUG:CAPICE:NaN detected in column baz, percentage: 25.0%.'
        ]
        imputer = CapiceImputing(self.model)
        with self.assertLogs(level=10) as captured:
            imputer._get_nan_ratio_per_column(dataset=nan_dataframe)
        self.assertGreater(len(captured.output), 0)
        for message in messages_present:
            self.assertIn(message, captured.output)


if __name__ == '__main__':
    unittest.main()
