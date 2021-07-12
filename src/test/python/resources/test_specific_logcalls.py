import unittest
import pandas as pd
from datetime import datetime
from src.main.python.resources.imputers.cadd_imputing import CaddImputing
from src.test.python.test_templates import set_up_manager_and_loc, teardown
import sys
import io


class TestSpecificLogCalls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.manager, cls.output_loc = set_up_manager_and_loc()
        cls.manager.critical_logging_only = False
        cls.manager.verbose = True
        cls.manager.enable_logfile = False
        cls.manager.log_loc = cls.output_loc
        cls.manager.now = datetime.now()

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        teardown()

    def setUp(self):
        print('Testing case:')

    def test_nan_calculator(self):
        print('Nan calculator (using piping of stderr to variable)')
        old_stdout = sys.stderr
        new_stdout = io.StringIO()
        sys.stderr = new_stdout
        nan_dataframe = pd.DataFrame(
            {
                'foo': [1, 2, 3, 4],
                'bar': [55, None, None, 66],
                'baz': [None, 77, 88, 99]
            }
        )
        messages_present = ['[CAPICE] [test_specific_logcalls.py] [test_nan_calculator] [DEBU]  '
                            'NaN detected in column bar, percentage: 50.0%.',
                            '[CAPICE] [test_specific_logcalls.py] [test_nan_calculator] [DEBU]  '
                            'NaN detected in column baz, percentage: 25.0%.']
        self.manager.cadd_version = 1.4
        self.manager.grch_build = 37
        imputer = CaddImputing()
        imputer._get_nan_ratio_per_column(dataset=nan_dataframe)
        log_messages = new_stdout.getvalue().splitlines()
        sys.stderr = old_stdout
        stripped_log_messages = []
        for message in log_messages[-2:]:  # Only the last 2 log messages are of interest.
            stripped_log_messages.append(' '.join(message.strip().split(' ')[2:]))  # Cryptic way to remove timestamp.
        for message in stripped_log_messages:
            self.assertIn(message, messages_present)


if __name__ == '__main__':
    unittest.main()
