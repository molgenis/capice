import unittest
import pandas as pd

from molgenis.capice.vep.splice_ai import SpliceAI
from molgenis.capice.utilities.enums import Column


class TestSpliceAI(unittest.TestCase):
    def test_splice_ai(self):
        processor = SpliceAI()
        dataset = pd.DataFrame(
            {
                'SpliceAI_pred_SYMBOL': ['foo', 'bar', 'baz'],
                Column.gene_name.value: ['foo', 'baz', 'bar']
            }
        )
        expected = pd.concat(
            [
                dataset,
                pd.DataFrame(
                    {
                        'SpliceAI_pred_SYMBOL_match': [1, 0, 0]
                    }
                )
            ], axis=1
        )
        observed = processor.process(dataset)
        pd.testing.assert_frame_equal(observed, expected)


if __name__ == '__main__':
    unittest.main()
