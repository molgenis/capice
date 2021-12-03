import os
import unittest

import pandas as pd

from src.main.python.utilities.input_parser import InputParser
from src.main.python.utilities.utilities import get_project_root_dir


class TestInputParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.parser = InputParser()

    def test_parse(self):
        self.parser.set_separator(',')
        input_file = self.parser.parse(
            os.path.join(get_project_root_dir(), 'src', 'test', 'resources', 'input_parser',
                         'input_parser.txt'))
        expected_df = pd.DataFrame(
            {
                'this': ['this'],
                'is': ['is'],
                'a': ['a'],
                'header': ['line']
            }
        )
        pd.testing.assert_frame_equal(input_file, expected_df)

        if __name__ == '__main__':
            unittest.main()
