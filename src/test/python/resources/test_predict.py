import os
import pickle
import unittest
from src.main.python.resources.utilities.utilities import get_project_root_dir
from src.test.python.test_templates import set_up_manager_and_loc, teardown, \
    set_up_main
from src.main.python.resources.enums.sections import Column


class TestPredict(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        manager, output_loc = set_up_manager_and_loc()
        cls.main = set_up_main()
        cls.main.infile = os.path.join(get_project_root_dir(),
                                       'CAPICE_example',
                                       'CAPICE_input.tsv.gz')
        with open(
                os.path.join(
                    get_project_root_dir(),
                    'CAPICE_model',
                    'GRCh37',
                    'POC',
                    'xgb_booster_poc.pickle.dat'
                ), 'rb'
        ) as model_file:
            cls.main.model = pickle.load(model_file)

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
            self.main.preprocess(
                self.main.impute(
                    self.main.process(
                        self.main.load_file()
                    )
                ), train=False
            )
        )

    def test_component_prediction(self):
        """
        Component test for prediction to see if the combined score of all is
        greater than 0.
        """
        print('Prediction (component)')
        prediction = self.main.predict(
            self.main.preprocess(
                self.main.impute(
                    self.main.process(
                        self.main.load_file()
                    )
                ), train=False
            )
        )
        # Combined sum of the prediction score should be higher than 0
        self.assertGreater(prediction[Column.score.value].sum(), 0)


if __name__ == '__main__':
    unittest.main()
