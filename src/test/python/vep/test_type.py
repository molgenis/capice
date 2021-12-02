import unittest

import pandas as pd

from src.main.python.vep import type


class TestType(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.type = type.Type()

    def test_process(self):
        input_data_frame = pd.DataFrame({'ref': ['C', 'CA', 'CA', 'C', 'CA', 'CA'],
                                         'alt': ['G', 'GCC', 'GG', 'CG', 'G', 'C']})
        actual_output = self.type.process(input_data_frame)
        expected_output = pd.DataFrame({
            'ref': ['C', 'CA', 'CA', 'C', 'CA', 'CA'],
            'alt': ['G', 'GCC', 'GG', 'CG', 'G', 'C'],
            'Type': ['SNV', 'DELINS', 'DELINS', 'INS', 'DELINS', 'DEL']})
        pd.testing.assert_frame_equal(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
