import unittest

import pandas as pd

from molgenis.capice.vep import type


class TestType(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.type = type.Type()

    def test_process(self):
        input_data_frame = pd.DataFrame({'REF': ['C', 'CA', 'CA', 'C', 'CA', 'CA'],
                                         'ALT': ['G', 'GCC', 'GG', 'CG', 'G', 'C']})
        actual_output = self.type.process(input_data_frame)
        expected_output = pd.DataFrame({
            'REF': ['C', 'CA', 'CA', 'C', 'CA', 'CA'],
            'ALT': ['G', 'GCC', 'GG', 'CG', 'G', 'C'],
            'Type': ['SNV', 'DELINS', 'DELINS', 'INS', 'DELINS', 'DEL']})
        expected_output = expected_output.astype({'Type': 'category'})

        pd.testing.assert_frame_equal(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
