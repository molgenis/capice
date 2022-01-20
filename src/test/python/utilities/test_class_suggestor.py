import unittest

import pandas as pd

from src.main.python.utilities.enums import Column, OutputClasses
from src.main.python.utilities.class_suggestor import ClassSuggestor


class TestClassSuggestor(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dataset = pd.DataFrame(
            {
                'gene_name': ['foo', 'TTN', 'COL7A1', 'MEFV', 'bar'],
                'score': [0.9234, 0.2134, 0.0012, 0.4563, 0.7854]
            }
        )

    def test_apply_suggestion(self):
        suggestor = ClassSuggestor()
        copy_dataset = self.dataset.copy(deep=True)
        observed = suggestor.apply_suggestion(copy_dataset)
        expected = pd.concat(
            [
                self.dataset,
                pd.DataFrame(
                    {
                        'suggested_class': ['VUS', 'VUS', 'VUS', 'VUS', 'VUS']
                    }
                )
            ], axis=1
        )
        pd.testing.assert_frame_equal(observed, expected)


if __name__ == '__main__':
    unittest.main()
