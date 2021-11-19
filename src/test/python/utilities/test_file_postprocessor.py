import unittest
import pandas as pd

from src.test.python.test_templates import teardown, set_up_manager_and_out
from src.main.python.utilities.load_file_postprocessor import \
    LoadFilePostProcessor


class TestFilePostProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print('Setting up.')
        set_up_manager_and_out()

    @classmethod
    def tearDownClass(cls) -> None:
        print('Tearing down.')
        teardown()

    def setUp(self) -> None:
        print('Testing case:')

    def test_load_file_pre_processor(self):
        """
        Test to see if the post file loading processor outputs according to
        expectation. Note: chromosome stays an integer un till the imputer,
        that's why I don't mark them as string.
        """
        print('Load file preprocessor.')
        data = pd.DataFrame(
            {
                "%CHROM": [1, 2, 3],
                "%POS": [100, 200, 300],
                "%REF": ['A', 'T', 'G'],
                "%ALT": ['T', 'G', 'A'],
                "%SYMBOL_SOURCE": ['foo', 'foo', 'bar'],
                "%Feature": ['bar', 'bar', 'buz'],
                "%SYMBOL": ['g1', 'g2', 'g3'],
                "%INTRON": [1, 0, 0],
                "%EXON": [0, 1, 1]
            }
        )

        expected_output = pd.DataFrame(
            {
                "chr": [1, 2, 3],
                "pos": [100, 200, 300],
                "ref": ['A', 'T', 'G'],
                "alt": ['T', 'G', 'A'],
                "id_source": ['foo', 'foo', 'bar'],
                "transcript": ['bar', 'bar', 'buz'],
                "gene_name": ['g1', 'g2', 'g3'],
                "Intron": [1, 0, 0],
                "Exon": [0, 1, 1]
            }
        )

        processor = LoadFilePostProcessor(dataset=data)
        observed_output = processor.process()
        pd.testing.assert_frame_equal(expected_output, observed_output)


if __name__ == '__main__':
    unittest.main()
