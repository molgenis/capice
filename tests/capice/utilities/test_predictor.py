import unittest

from molgenis.capice.utilities.predictor import Predictor
from tests.capice.test_templates import set_up_impute_preprocess


class TestPredictor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        main, model = set_up_impute_preprocess()
        cls.predictor = Predictor(model)
        cls.dataset = main.categorical_process(
            main.process(
                main._load_file()
            ), processing_features=model.processable_features
        )[0]

    def test_predict(self):
        observed = self.predictor.predict(self.dataset)
        self.assertGreater(observed['score'].sum(), 0)
        self.assertFalse(observed['score'].hasnans)


if __name__ == '__main__':
    unittest.main()
