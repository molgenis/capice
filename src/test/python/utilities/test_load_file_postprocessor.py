import unittest
import pandas as pd

from src.main.python.utilities.load_file_postprocessor import LoadFilePostProcessor


class LoadFilePostprocessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        df = pd.DataFrame(
            {
                '#CHROM': [1],
                'POS': [123],
                'REF': ['A'],
                'ALT': ['G'],
                'HGNC_ID': [123],
                'SYMBOL_SOURCE': ['hgnc'],
                '%Feature': ['NM1.123'],
                'SYMBOL': ['ACDC'],
                'INTRON': [5],
                'EXON': [11],
                'MAX_AF': [6]
            }
        )
        cls.processor = LoadFilePostProcessor(df)

    def test_process(self):
        observed = self.processor.process()
        expected = pd.DataFrame(
            {
                'chr': [1],
                'pos': [123],
                'ref': ['A'],
                'alt': ['G'],
                'gene_id': [123],
                'id_source': ['hgnc'],
                'transcript': ['NM1.123'],
                'gene_name': ['ACDC'],
                'Intron': [5],
                'Exon': [11],
                'max_AF': [6]
            }
        )
        pd.testing.assert_frame_equal(expected, observed)


if __name__ == '__main__':
    unittest.main()
