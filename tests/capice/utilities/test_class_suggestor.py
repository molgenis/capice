import unittest

import pandas as pd

from molgenis.capice.utilities.enums import Column, OutputClasses
from molgenis.capice.utilities.class_suggestor import ClassSuggestor


class TestClassSuggestor(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dataset = pd.DataFrame(
            {
                Column.gene_name.value: ['foo', 'TTN', 'COL7A1', 'MEFV', 'bar'],
                Column.score.value: [0.9234, 0.2134, 0.0012, 0.4563, 0.7854]
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
                        Column.suggested_class.value: [
                            OutputClasses.unknown.value,
                            OutputClasses.unknown.value,
                            OutputClasses.unknown.value,
                            OutputClasses.unknown.value,
                            OutputClasses.unknown.value
                        ]
                    }
                )
            ], axis=1
        )
        pd.testing.assert_frame_equal(observed, expected)


if __name__ == '__main__':
    unittest.main()
