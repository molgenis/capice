import unittest

import numpy as np
import pandas as pd

from molgenis.capice.vep.consequence import Consequence


class TestConsequence(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.consequence = Consequence()

    def test_process(self):
        dataframe = pd.DataFrame({
            'Consequence': ['transcript_ablation&stop_lost', 'start_lost', np.nan]
        })
        observed = self.consequence.process(dataframe)
        expected = pd.DataFrame({
            'Consequence': ['transcript_ablation&stop_lost', 'start_lost', np.nan],
            'most_severe_consequence': ['transcript_ablation', 'start_lost', np.nan],
        })
        expected = expected.astype({
            'Consequence': 'object', 'most_severe_consequence': 'category'
        })
        pd.testing.assert_frame_equal(expected, observed)

    def test_non_coding(self):
        data = pd.DataFrame({
            'variants': ['variant_1', 'variant_2', 'variant_3'],
            'Consequence': [np.nan, np.nan, np.nan]
        })
        columns = data.columns
        expected_altered = self.expected_data.copy(deep=True)
        # Easier to locate the ones in self.expected_data than to hardcode a new one
        expected_altered.loc[1, 'is_start_lost'] = 0
        expected_altered.loc[0, 'is_stop_lost'] = 0
        expected_altered.loc[0, 'is_transcript_ablation'] = 0
        expected = pd.concat([data, expected_altered], axis=1)
        observed = Consequence().process(data)
        self.assertFalse(observed[observed.columns.difference(columns)].isnull().values.any())
        pd.testing.assert_frame_equal(
            observed.sort_index(axis=1),
            expected.sort_index(axis=1)
        )

    def test_consequence_warning(self):
        """
        Tests that when a consequence is encountered that is not present within the processor
        raises a warning.
        """
        dataframe = pd.DataFrame(
            {
                'Consequence': ['transcript_ablation&stop_lost', 'start_lost', 'fake_consequence']
            }
        )
        dataframe_copy = dataframe.copy(deep=True)
        with self.assertLogs() as captured:
            observed = Consequence().process(dataframe)
        expected = pd.concat(
            [
                dataframe_copy,
                self.expected_data
            ], axis=1
        )

        pd.testing.assert_frame_equal(observed.sort_index(axis=1), expected.sort_index(
            axis=1), check_dtype=False)
        self.assertEqual('Supplied VEP consequence: fake_consequence is not supported in the '
                         'Consequence processor!', captured.records[0].getMessage())


if __name__ == '__main__':
    unittest.main()
