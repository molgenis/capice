import unittest

import pandas as pd
import numpy as np

from tests.capice.test_templates import set_up_manager_and_out, teardown
from molgenis.capice.utilities.manual_vep_processor import ManualVEPProcessor


class TestAnnotator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        set_up_manager_and_out()
        # Creating a dataframe of data that is tailored to test the
        # return N append function within lookup.py.
        cls.dataset = pd.DataFrame(
            {
                'chr': {0: '1', 1: '1'},
                'pos': {0: 1, 1: 10042538},
                'REF': {0: 'C', 1: 'C'},
                'ALT': {0: 'T', 1: 'T'},
                'Consequence': {0: 'missense_variant', 1: 'downstream_gene_variant'},
                'gene_name': {0: 'NMNAT1', 1: 'NMNAT1'},
                'SourceID': {0: 'HGNC', 1: 'HGNC'},
                'HGNC_ID': {0: '17877', 1: '17877'},
                'FeatureID': {0: 'ENST00000377205', 1: 'ENST00000403197'},
                'cDNA_position': {0: '763/3781', 1: np.nan},
                'CDS_position': {0: '619/840', 1: np.nan},
                'Protein_position': {0: '207/279', 1: np.nan},
                'Amino_acids': {0: 'R/W', 1: np.nan},
                'STRAND': {0: 1, 1: 1},
                'SIFT': {0: 0.04, 1: np.nan},
                'PolyPhen': {0: 0.08, 1: np.nan},
                'Exon': {0: '5/5', 1: np.nan},
                'Intron': {0: np.nan, 1: np.nan}
            }
        )
        cls.annotator = ManualVEPProcessor()
        cls.user_input_features = ['REF', 'PolyPhen', 'SIFT', 'Consequence', 'cDNA_position',
                                   'CDS_position', 'Protein_position', 'Amino_acids']

    def setUp(self) -> None:
        print('Testing case:')

    @classmethod
    def tearDownClass(cls) -> None:
        print('Tearing down.')
        teardown()

    def test_component_annotator(self):
        print('Processor (component)')
        expected_processed_columns = pd.DataFrame(
            {
                'SIFTcat': {0: 'deleterious', 1: np.nan},
                'SIFTval': {0: 0.04, 1: np.nan},
                'CDSpos': {0: 619.0, 1: np.nan},
                'relCDSpos': {0: 840.0, 1: np.nan},
                'PolyPhenCat': {0: 'benign', 1: np.nan},
                'PolyPhenVal': {0: 0.08, 1: np.nan},
                'oAA': {0: 'R', 1: np.nan},
                'nAA': {0: 'W', 1: np.nan},
                'cDNApos': {0: 763.0, 1: np.nan},
                'relcDNApos': {0: 3781.0, 1: np.nan},
                'protPos': {0: 207.0, 1: np.nan},
                'relProtPos': {0: 279.0, 1: np.nan},
                'is_regulatory_region_variant': {0: 0, 1: 0},
                'is_regulatory_region_ablation': {0: 0, 1: 0},
                'is_regulatory_region_amplification': {0: 0, 1: 0},
                'is_missense_variant': {0: 1, 1: 0}, 'is_intron_variant': {0: 0, 1: 0},
                'is_upstream_gene_variant': {0: 0, 1: 0},
                'is_downstream_gene_variant': {0: 0, 1: 1}, 'is_synonymous_variant': {0: 0, 1: 0},
                'is_TF_binding_site_variant': {0: 0, 1: 0}, 'is_splice_donor_variant': {0: 0, 1: 0},
                'is_coding_sequence_variant': {0: 0, 1: 0},
                'is_splice_region_variant': {0: 0, 1: 0}, 'is_stop_gained': {0: 0, 1: 0},
                'is_splice_acceptor_variant': {0: 0, 1: 0}, 'is_frameshift_variant': {0: 0, 1: 0},
                'is_3_prime_UTR_variant': {0: 0, 1: 0}, 'is_inframe_insertion': {0: 0, 1: 0},
                'is_inframe_deletion': {0: 0, 1: 0}, 'is_5_prime_UTR_variant': {0: 0, 1: 0},
                'is_start_lost': {0: 0, 1: 0},
                'is_non_coding_transcript_exon_variant': {0: 0, 1: 0},
                'is_non_coding_transcript_variant': {0: 0, 1: 0}, 'is_TFBS_ablation': {0: 0, 1: 0},
                'is_TFBS_amplification': {0: 0, 1: 0}, 'is_protein_altering_variant': {0: 0, 1: 0},
                'is_stop_lost': {0: 0, 1: 0}, 'is_stop_retained_variant': {0: 0, 1: 0},
                'is_transcript_ablation': {0: 0, 1: 0}, 'is_intergenic_variant': {0: 0, 1: 0},
                'is_start_retained_variant': {0: 0, 1: 0},
                'is_transcript_amplification': {0: 0, 1: 0},
                'is_incomplete_terminal_codon_variant': {0: 0, 1: 0},
                'is_mature_miRNA_variant': {0: 0, 1: 0},
                'is_NMD_transcript_variant': {0: 0, 1: 0},
                'is_feature_elongation': {0: 0, 1: 0},
                'is_feature_truncation': {0: 0, 1: 0},
                'is_splice_donor_5th_base_variant': {0: 0, 1: 0},
                'is_splice_donor_region_variant': {0: 0, 1: 0},
                'is_splice_polypyrimidine_tract_variant': {0: 0, 1: 0},
                'Type': {0: 'SNV', 1: 'SNV'},
                'Length': {0: 0, 1: 0}
            }
        )
        expected_processed_columns = expected_processed_columns.astype({
            'SIFTcat': 'category',
            'SIFTval': 'float64',
            'CDSpos': 'Int64',
            'relCDSpos': 'Int64',
            'PolyPhenCat': 'category',
            'PolyPhenVal': 'float64',
            'oAA': 'category',
            'nAA': 'category',
            'cDNApos': 'Int64',
            'relcDNApos': 'Int64',
            'protPos': 'Int64',
            'relProtPos': 'Int64',
            'is_regulatory_region_variant': 'boolean',
            'is_regulatory_region_ablation': 'boolean',
            'is_regulatory_region_amplification': 'boolean',
            'is_missense_variant': 'boolean',
            'is_upstream_gene_variant': 'boolean',
            'is_downstream_gene_variant': 'boolean',
            'is_TF_binding_site_variant': 'boolean',
            'is_coding_sequence_variant': 'boolean',
            'is_splice_region_variant': 'boolean',
            'is_splice_acceptor_variant': 'boolean',
            'is_3_prime_UTR_variant': 'boolean',
            'is_inframe_deletion': 'boolean',
            'is_start_lost': 'boolean',
            'is_non_coding_transcript_exon_variant': 'boolean',
            'is_non_coding_transcript_variant': 'boolean',
            'is_TFBS_amplification': 'boolean',
            'is_stop_lost': 'boolean',
            'is_transcript_ablation': 'boolean',
            'is_start_retained_variant': 'boolean',
            'is_transcript_amplification': 'boolean',
            'is_incomplete_terminal_codon_variant': 'boolean',
            'is_mature_miRNA_variant': 'boolean',
            'is_NMD_transcript_variant': 'boolean',
            'is_feature_elongation': 'boolean',
            'is_feature_truncation': 'boolean',
            'is_splice_donor_5th_base_variant': 'boolean',
            'is_splice_donor_region_variant': 'boolean',
            'is_splice_polypyrimidine_tract_variant': 'boolean',
            'Type': 'category',
            'Length': 'Int64'
        })
        expected_outcome = pd.concat(
            [
                self.dataset[
                    [
                        'chr',
                        'pos',
                        'REF',
                        'ALT',
                        'gene_name',
                        'SourceID',
                        'HGNC_ID',
                        'FeatureID',
                        'STRAND',
                        'Exon',
                        'Intron'
                    ]
                ],
                expected_processed_columns
            ], axis=1
        )
        outcome = self.annotator.process(self.dataset, self.user_input_features)
        # if numpy.array dtype not given,
        # then the type will be determined as the minimum type required to hold the
        # objects in the sequence. this minimal type is system dependent.
        pd.testing.assert_frame_equal(
            expected_outcome.sort_index(axis=1), outcome.sort_index(axis=1), check_dtype=False
        )

    def test_bug_attributeerror_template_sift_polyphen(self):
        print('Testing bug "AttributeError: Can only use .str accessor with '
              'string values!" within template_sift_polyphen manual annotator.')
        bugged_dataframe = pd.DataFrame(
            {
                'chr': ['1', '2'],
                'pos': [100, 200],
                'REF': ['A', 'GCC'],
                'ALT': ['C', 'C'],
                'SIFT': [np.nan, np.nan],
                'PolyPhen': [np.nan, np.nan]
            }
        )
        bugged_dataframe = bugged_dataframe.astype({
            'chr': 'string',
            'pos': 'int64',
            'REF': 'string',
            'ALT': 'string',
            'SIFT': 'float64',
            'PolyPhen': 'float64',
        })

        expected_dataframe = pd.DataFrame(
            {
                'chr': ['1', '2'],
                'pos': [100, 200],
                'REF': ['A', 'GCC'],
                'ALT': ['C', 'C'],
                'SIFTcat': [np.nan, np.nan],
                'SIFTval': [np.nan, np.nan],
                'PolyPhenCat': [np.nan, np.nan],
                'PolyPhenVal': [np.nan, np.nan]
            }
        )
        expected_dataframe = expected_dataframe.astype({
            'chr': 'string',
            'pos': 'int64',
            'REF': 'string',
            'ALT': 'string',
            'SIFTcat': 'category',
            'SIFTval': 'float64',
            'PolyPhenCat': 'category',
            'PolyPhenVal': 'float64'
        })
        annotator = ManualVEPProcessor()
        out_dataframe = annotator.process(bugged_dataframe, self.user_input_features)
        # Testing for expected dataframe columns, since it processes more.
        pd.testing.assert_frame_equal(expected_dataframe, out_dataframe[expected_dataframe.columns])

    @staticmethod
    def prepare_getter_tests():
        data = pd.DataFrame(
            {
                'REF': ['A', 'C'],
                'ALT': ['T', 'G'],
                'PolyPhen': [0.08, 0.98]
            }
        )
        user_input = ['REF', 'PolyPhen']
        annotator = ManualVEPProcessor()
        annotator.process(data, user_input)
        return annotator

    def test_getter_vep_input(self):
        data = pd.DataFrame(
            {
                'REF': ['A', 'C'],
                'ALT': ['T', 'G'],
                'PolyPhen': [0.08, 0.98]
            }
        )
        user_input = ['REF', 'PolyPhen']
        annotator = ManualVEPProcessor()
        annotator.process(data, user_input)
        observed = annotator.get_feature_processes()
        expected_keys = ['REF', 'PolyPhen']
        expected_values = ['Type', 'Length', 'PolyPhenCat', 'PolyPhenVal']
        for input_feature in observed.keys():
            self.assertIn(input_feature, expected_keys)
        for output_features in observed.values():
            for feature in output_features:
                self.assertIn(feature, expected_values)


if __name__ == '__main__':
    unittest.main()
