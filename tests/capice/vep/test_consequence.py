import unittest

import numpy as np
import pandas as pd

from molgenis.capice.vep.consequence import Consequence


class TestConsequence(unittest.TestCase):
    def setUp(self) -> None:
        self.data = pd.DataFrame(
            {
                'Consequence': ['transcript_ablation&stop_lost', 'start_lost', np.nan]
            }
        )
        self.expected_data = pd.DataFrame(
                    {
                        'is_regulatory_region_variant': {0: 0, 1: 0, 2: 0},
                        'is_regulatory_region_ablation': {0: 0, 1: 0, 2: 0},
                        'is_regulatory_region_amplification': {0: 0, 1: 0, 2: 0},
                        'is_missense_variant': {0: 0, 1: 0, 2: 0},
                        'is_intron_variant': {0: 0, 1: 0, 2: 0},
                        'is_upstream_gene_variant': {0: 0, 1: 0, 2: 0},
                        'is_downstream_gene_variant': {0: 0, 1: 0, 2: 0},
                        'is_synonymous_variant': {0: 0, 1: 0, 2: 0},
                        'is_TF_binding_site_variant': {0: 0, 1: 0, 2: 0},
                        'is_splice_donor_variant': {0: 0, 1: 0, 2: 0},
                        'is_coding_sequence_variant': {0: 0, 1: 0, 2: 0},
                        'is_splice_region_variant': {0: 0, 1: 0, 2: 0},
                        'is_stop_gained': {0: 0, 1: 0, 2: 0},
                        'is_splice_acceptor_variant': {0: 0, 1: 0, 2: 0},
                        'is_frameshift_variant': {0: 0, 1: 0, 2: 0},
                        'is_3_prime_UTR_variant': {0: 0, 1: 0, 2: 0},
                        'is_inframe_insertion': {0: 0, 1: 0, 2: 0},
                        'is_inframe_deletion': {0: 0, 1: 0, 2: 0},
                        'is_5_prime_UTR_variant': {0: 0, 1: 0, 2: 0},
                        'is_start_lost': {0: 0, 1: 1, 2: 0},
                        'is_non_coding_transcript_exon_variant': {0: 0, 1: 0, 2: 0},
                        'is_non_coding_transcript_variant': {0: 0, 1: 0, 2: 0},
                        'is_TFBS_ablation': {0: 0, 1: 0, 2: 0},
                        'is_TFBS_amplification': {0: 0, 1: 0, 2: 0},
                        'is_protein_altering_variant': {0: 0, 1: 0, 2: 0},
                        'is_stop_lost': {0: 1, 1: 0, 2: 0},
                        'is_stop_retained_variant': {0: 0, 1: 0, 2: 0},
                        'is_transcript_ablation': {0: 1, 1: 0, 2: 0},
                        'is_intergenic_variant': {0: 0, 1: 0, 2: 0},
                        'is_start_retained_variant': {0: 0, 1: 0, 2: 0},
                        'is_transcript_amplification': {0: 0, 1: 0, 2: 0},
                        'is_incomplete_terminal_codon_variant': {0: 0, 1: 0, 2: 0},
                        'is_mature_miRNA_variant': {0: 0, 1: 0, 2: 0},
                        'is_NMD_transcript_variant': {0: 0, 1: 0, 2: 0},
                        'is_feature_elongation': {0: 0, 1: 0, 2: 0},
                        'is_feature_truncation': {0: 0, 1: 0, 2: 0},
                        'is_splice_donor_5th_base_variant': {0: 0, 1: 0, 2: 0},
                        'is_splice_donor_region_variant': {0: 0, 1: 0, 2: 0},
                        'is_splice_polypyrimidine_tract_variant': {0: 0, 1: 0, 2: 0}
                    }

                )

    def test_consequence(self):
        data_copy = self.data.copy(deep=True)
        observerd = Consequence().process(self.data)
        # if numpy.array dtype not given,
        # then the type will be determined as the minimum type required to hold the
        # objects in the sequence. this minimal type is system dependent.
        expected = pd.concat(
            [
                data_copy,
                self.expected_data
            ], axis=1
        )
        pd.testing.assert_frame_equal(observerd.sort_index(axis=1), expected.sort_index(
            axis=1), check_dtype=False)

    def test_non_coding(self):
        data = pd.DataFrame({
            'variants': ['variant_1', 'variant_2', 'variant_3'],
            'Consequence': [np.nan, np.nan, np.nan]
        })
        columns = data.columns
        expected = pd.concat([data, self.expected_data], axis=1)
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
