import pandas as pd
import numpy as np
import unittest
from src.main.python.resources.annotaters.annotator import Annotator
from src.test.python.test_templates import set_up_manager_and_loc, teardown


class TestAnnotator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        set_up_manager_and_loc()
        # Creating a dataframe of data that is tailored to test the
        # return N append function within lookup.py.
        dataset = pd.DataFrame(
            {
                'Chr': {0: '1', 1: '1'},
                'Pos': {0: 1, 1: 10042538},
                'Ref': {0: 'C', 1: 'C'},
                'Alt': {0: 'T', 1: 'T'},
                'Consequence': {0: 'missense_variant',
                                1: 'downstream_gene_variant'
                                },
                'GeneName': {0: 'NMNAT1', 1: 'NMNAT1'},
                'SourceID': {0: 'HGNC', 1: 'HGNC'},
                'HGNC_ID': {0: '17877', 1: '17877'},
                'FeatureID': {0: 'ENST00000377205', 1: 'ENST00000403197'},
                'cDNA_position': {0: '763/3781', 1: np.nan},
                'CDS_position': {0: '619/840', 1: np.nan},
                'Protein_position': {0: '207/279', 1: np.nan},
                'Amino_acids': {0: 'R/W', 1: np.nan},
                'STRAND': {0: 1, 1: 1},
                'SIFT': {0: 'deleterious(0.04)', 1: np.nan},
                'PolyPhen': {0: 'benign(0.08)', 1: np.nan},
                'DOMAINS': {
                    0: 'PANTHER:PTHR12039&'
                       'PANTHER:PTHR12039:SF3&'
                       'TIGRFAM:TIGR00482&'
                       'Gene3D:3.40.50.620&'
                       'Pfam:PF01467&'
                       'Superfamily:SSF52374',
                    1: np.nan
                },
                'MOTIF_NAME': {0: np.nan, 1: np.nan},
                'HIGH_INF_POS': {0: np.nan, 1: np.nan},
                'MOTIF_SCORE_CHANGE': {0: np.nan, 1: np.nan},
                'Exon': {0: '5/5', 1: np.nan},
                'Intron': {0: np.nan, 1: np.nan}
            }
        )
        cls.annotator = Annotator(dataset)

    def setUp(self) -> None:
        print('Testing case:')

    @classmethod
    def tearDownClass(cls) -> None:
        print('Tearing down.')
        teardown()

    def test_component_annotator(self):
        print('Annotator (component)')
        expected_outcome = pd.DataFrame(
            {'Chr': {0: '1', 1: '1'}, 'Pos': {0: 1, 1: 10042538},
             'Ref': {0: 'C', 1: 'C'}, 'Alt': {0: 'T', 1: 'T'},
             'Consequence': {0: 'missense_variant',
                             1: 'downstream_gene_variant'},
             'GeneName': {0: 'NMNAT1', 1: 'NMNAT1'},
             'SourceID': {0: 'HGNC', 1: 'HGNC'},
             'HGNC_ID': {0: '17877', 1: '17877'},
             'FeatureID': {0: 'ENST00000377205', 1: 'ENST00000403197'},
             'STRAND': {0: 1, 1: 1},
             'Exon': {0: '5/5', 1: np.nan},
             'Intron': {0: np.nan, 1: np.nan},
             'motifEScoreChng': {0: np.nan, 1: np.nan},
             'SIFTcat': {0: 'deleterious', 1: np.nan},
             'SIFTval': {0: 0.04, 1: np.nan},
             'CDSpos': {0: 619.0, 1: np.nan},
             'relCDSpos': {0: 840.0, 1: np.nan},
             'PolyPhenCat': {0: 'benign', 1: np.nan},
             'PolyPhenVal': {0: 0.08, 1: np.nan},
             'Domain': {0: 'hmmpanther', 1: None},
             'Length': {0: 0, 1: 0},
             'oAA': {0: 'R', 1: np.nan},
             'nAA': {0: 'W', 1: np.nan},
             # 'GC': {0: 0.41, 1: 0.46},
             # 'CpG': {0: 0.020134228187919462, 1: 0.08053691275167785},
             'motifEName': {0: np.nan, 1: np.nan},
             'motifECount': {0: None, 1: None},
             'Type': {0: 'SNV', 1: 'SNV'},
             'cDNApos': {0: 763.0, 1: np.nan},
             'relcDNApos': {0: 3781.0, 1: np.nan},
             'motifEHIPos': {0: 0, 1: 0},
             'protPos': {0: 207.0, 1: np.nan},
             'relProtPos': {0: 279.0, 1: np.nan},
             'ConsDetail': {0: 'missense', 1: 'downstream'}
             }
        )
        outcome = self.annotator.annotate()
        pd.testing.assert_frame_equal(
            expected_outcome.sort_index(axis=1), outcome.sort_index(axis=1)
        )

    def test_bug_attributeerror_template_sift_polyphen(self):
        print('Testing bug "AttributeError: Can only use .str accessor with '
              'string values!" within template_sift_polyphen manual annotator.')
        bugged_dataframe = pd.DataFrame(
            {
                'Chr': ['1', '2'],
                'Pos': [100, 200],
                'Ref': ['A', 'GCC'],
                'Alt': ['C', 'C'],
                'SIFT': [np.nan, np.nan],
                'PolyPhen': [np.nan, np.nan]
            }
        )

        expected_dataframe = pd.DataFrame(
            {
                'Chr': ['1', '2'],
                'Pos': [100, 200],
                'Ref': ['A', 'GCC'],
                'Alt': ['C', 'C'],
                'SIFTcat': [np.nan, np.nan],
                'SIFTval': [np.nan, np.nan],
                'PolyPhenCat': [np.nan, np.nan],
                'PolyPhenVal': [np.nan, np.nan]
            }
        )
        annotator = Annotator(bugged_dataframe)
        out_dataframe = annotator.annotate()
        # Testing for expected dataframe columns, since it processes more.
        pd.testing.assert_frame_equal(
            expected_dataframe,
            out_dataframe[expected_dataframe.columns]
        )


if __name__ == '__main__':
    unittest.main()
