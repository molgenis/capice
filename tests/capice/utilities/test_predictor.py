import unittest

import numpy as np
import pandas as pd

from molgenis.capice.utilities.predictor import Predictor
from tests.capice.test_templates import set_up_impute_preprocess


class TestPredictor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        main, model = set_up_impute_preprocess()
        cls.predictor = Predictor(model)
        cls.dataset = main.preprocess(
            main.impute(
                main.process(
                    main._load_file()
                ), impute_values=model.impute_values
            ), model_features=model.get_booster().feature_names
        )

    def test_predict(self):
        observed = self.predictor.predict(self.dataset)
        expected = pd.Series(
            [0.3761149048805237, 0.19460521638393402, 0.3761149048805237, 0.3761149048805237,
             0.5323305726051331, 0.5323305726051331, 0.3761149048805237]).astype(
            np.float32).rename('score')
        pd.testing.assert_series_equal(expected, observed['score'])


if __name__ == '__main__':
    unittest.main()
