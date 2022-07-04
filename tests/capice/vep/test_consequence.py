import unittest

import numpy as np
import pandas as pd

from molgenis.capice.vep.consequence import Consequence


class TestConsequence(unittest.TestCase):
    def test_consequence(self):
        dataframe = pd.DataFrame(
            {
                'Consequence': ['transcript_ablation&stop_lost', 'start_lost', np.nan]
            }
        )
        copy_dataframe = dataframe.copy(deep=True)
        observerd = Consequence().process(dataframe)
        expected = pd.concat(
            [
                copy_dataframe,
                pd.DataFrame(
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
                        'is_feature_truncation': {0: 0, 1: 0, 2: 0}}

                )
            ], axis=1
        )
        # if numpy.array dtype not given,
        # then the type will be determined as the minimum type required to hold the
        # objects in the sequence. this minimal type is system dependent.
        pd.testing.assert_frame_equal(observerd.sort_index(axis=1), expected.sort_index(axis=1),
                                      check_dtype=False)


if __name__ == '__main__':
    unittest.main()
