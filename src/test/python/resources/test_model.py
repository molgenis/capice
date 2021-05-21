import os
import unittest
from src.main.python.resources.utilities.utilities import get_project_root_dir
from src.test.python.test_templates import set_up_manager_and_loc, teardown, set_up_main


class TestModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        manager, output_loc = set_up_manager_and_loc()
        cls.main = set_up_main()
        cls.main.infile = os.path.join(get_project_root_dir(), 'CAPICE_example', 'test_cadd14_grch37_annotated.tsv.gz')
        manager.overwrite_model = 'CAPICE using XGBoost 0.72.1, CADD 1.4 and genome build 37.'

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
        preprocessing_instance, processed_file = self.main.preprocess(
            loaded_cadd_data=self.main.impute(
                loaded_cadd_data=self.main.load_file()
            ), train=False
        )
        self.main.predict(loaded_cadd_data=processed_file, preprocessing_instance=preprocessing_instance)

    def test_component_prediction(self):
        """
        Component test for prediction to see if the combined score of all is greater than 0.
        """
        print('Prediction (component)')
        preprocessing_instance, processed_file = self.main.preprocess(
            loaded_cadd_data=self.main.impute(
                loaded_cadd_data=self.main.load_file()
            ), train=False
        )
        prediction = self.main.predict(loaded_cadd_data=processed_file,
                                       preprocessing_instance=preprocessing_instance)
        # Combined sum of the prediction score should be higher than 0
        self.assertGreater(prediction['probabilities'].sum(), 0)


if __name__ == '__main__':
    unittest.main()
