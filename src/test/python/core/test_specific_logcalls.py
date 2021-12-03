import io
import os
import sys
import pickle
import unittest
import pandas as pd

from src.test.python.test_templates import teardown
from src.main.python.core.capice_manager import CapiceManager
from src.main.python.utilities.capice_imputing import CapiceImputing
from src.main.python.utilities.utilities import get_project_root_dir


class TestSpecificLogCalls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.manager = CapiceManager()
        cls.manager.loglevel = 10
        with open(
                os.path.join(
                    get_project_root_dir(),
                    'src',
                    'test',
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
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        nan_dataframe = pd.DataFrame(
            {
                'foo': [1, 2, 3, 4],
                'bar': [55, None, None, 66],
                'baz': [None, 77, 88, 99]
            }
        )
        messages_present = [
            'DEBUG: NaN detected in column bar, percentage: 50.0%.',
            'DEBUG: NaN detected in column baz, percentage: 25.0%.'
        ]
        imputer = CapiceImputing(self.model)
        imputer._get_nan_ratio_per_column(dataset=nan_dataframe)
        log_messages = new_stdout.getvalue().splitlines()
        sys.stdout = old_stdout
        stripped_log_messages = []
        # Only the last 2 log messages are of interest.
        for message in log_messages[-2:]:
            # Cryptic way to remove timestamp.
            stripped_log_messages.append(' '.join(message.strip().split(' ')[2:]))
        self.assertGreater(len(stripped_log_messages), 0)
        for message in stripped_log_messages:
            self.assertIn(message.lstrip(), messages_present)


if __name__ == '__main__':
    unittest.main()
