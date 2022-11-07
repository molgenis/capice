import unittest

import numpy as np
import pandas as pd

from molgenis.capice.vep.exon import Exon
from molgenis.capice.vep.intron import Intron


class TestIntronExon(unittest.TestCase):
    def setUp(self) -> None:
        self.test_set = pd.DataFrame(
            {
                'Exon': ['1/2', '4/5', np.nan, '3-4/7'],
                'Intron': ['1-2/6', '4/5', np.nan, '3/15'],
                'SomeOtherColumn': ['foo', 'bar', 'baz', 'barz']
            }
        )
        self.exon = Exon()
        self.intron = Intron()

    def test_exon_correct(self):
        expected = pd.concat(
            [
                self.test_set,
                pd.DataFrame(
                    {
                        'Exon_number': [1, 4, np.nan, 3],
                        'Exon_total': [2, 5, np.nan, 7],
                        'Exon_number_affected': [1, 1, np.nan, 2]
                    }
                ).astype('Int64')
            ], axis=1
        )
        observed = self.exon.process(self.test_set)
        pd.testing.assert_frame_equal(observed.sort_index(axis=1), expected.sort_index(axis=1))

    def test_intron_correct(self):
        expected = pd.concat(
            [
                self.test_set,
                pd.DataFrame(
                    {
                        'Intron_number': [1, 4, np.nan, 3],
                        'Intron_total': [6, 5, np.nan, 15],
                        'Intron_number_affected': [2, 1, np.nan, 1]
                    }
                ).astype('Int64')
            ], axis=1
        )
        observed = self.intron.process(self.test_set)
        pd.testing.assert_frame_equal(observed.sort_index(axis=1), expected.sort_index(axis=1))

    def test_only_snvs(self):
        test_set = pd.DataFrame(
            {
                'Exon': ['1/2', '4/5', np.nan, '3/7'],
                'Intron': ['1/6', '4/5', np.nan, '3/15'],
                'SomeOtherColumn': ['foo', 'bar', 'baz', 'barz']
            }
        )
        expected = pd.concat(
            [
                test_set,
                pd.DataFrame(
                    {
                        'Exon_number': [1, 4, np.nan, 3],
                        'Exon_total': [2, 5, np.nan, 7],
                        'Exon_number_affected': [1, 1, np.nan, 1]
                    }
                ).astype('Int64')
            ], axis=1
        )
        observed = self.exon.process(test_set)
        pd.testing.assert_frame_equal(observed.sort_index(axis=1), expected.sort_index(axis=1))

    def test_full_nan(self):
        test_set = pd.DataFrame(
            {
                'Exon': [np.nan, np.nan, np.nan],
                'Intron': [np.nan, np.nan, np.nan]
            }
        )
        expected = pd.concat(
            [
                test_set,
                pd.DataFrame(
                    {
                        'Exon_number': [np.nan, np.nan, np.nan],
                        'Exon_total': [np.nan, np.nan, np.nan],
                        'Exon_number_affected': [np.nan, np.nan, np.nan],
                        'Intron_number': [np.nan, np.nan, np.nan],
                        'Intron_total': [np.nan, np.nan, np.nan],
                        'Intron_number_affected': [np.nan, np.nan, np.nan]
                    }
                )
            ], axis=1
        )
        observed = self.exon.process(test_set)
        observed = self.intron.process(observed)
        pd.testing.assert_frame_equal(observed.sort_index(axis=1), expected.sort_index(axis=1))
