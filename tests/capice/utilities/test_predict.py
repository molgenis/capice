import unittest

from molgenis.capice.utilities.enums import Column
from tests.capice.test_templates import set_up_impute_preprocess, teardown


class TestPredict(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.main, cls.model = set_up_impute_preprocess()

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        teardown()

    def setUp(self):
        print('Testing case:')

    def test_unit_prediction(self):
        """
        Unit test for the prediction part of CAPICE.
        """
        print('Prediction (unit)')
        self.main.predict(
            self.main.categorical_process(
                self.main.process(
                    self.main._load_file()
                ), processing_features=self.model.processable_features
            )[0]
        )

    def test_component_prediction(self):
        """
        Component test for prediction to see if the combined score of all is
        greater than 0.
        """
        print('Prediction (component)')
        prediction = self.main.predict(
            self.main.categorical_process(
                self.main.process(
                    self.main._load_file()
                ), processing_features=self.model.processable_features
            )[0]
        )
        # Combined sum of the prediction score should be higher than 0
        self.assertGreater(prediction[Column.score.value].sum(), 0)


if __name__ == '__main__':
    unittest.main()
