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
            [0.49992973, 0.49992973, 0.5000119, 0.5001148]
        ).astype(np.float32).rename('score')
        # rtol = atol = 0.0005, because 0.5 * 10 ** -3 = 0.0005 for a tolerance of 3 decimals
        pd.testing.assert_series_equal(
            expected, observed['score'], check_exact=False, atol=0.0005, rtol=0.0005
        )


if __name__ == '__main__':
    unittest.main()
