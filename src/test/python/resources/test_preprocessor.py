import os
import unittest
from src.main.python.resources.utilities.utilities import get_project_root_dir
from src.test.python.test_templates import set_up_manager_and_loc, teardown, set_up_main


class TestPreprocessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.manager, output_loc = set_up_manager_and_loc()
        cls.main = set_up_main()
        cls.main.infile = os.path.join(get_project_root_dir(), 'CAPICE_example', 'test_cadd14_grch37_annotated.tsv.gz')
        cls.cadd_build = 1.4
        cls.grch_build = 37
        cls.impute_overwrite = 'CADD 1.4, GRCh build 37'
        cls.model_overwrite = 'CAPICE using XGBoost 0.72.1, CADD 1.4 and genome build 37.'

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        teardown()

    def setUp(self):
        print('Testing case:')

    def tearDown(self):
        print('Resetting arguments.')
        self.main.cla_cadd_version = False
        self.main.cla_genome_build = False
        self.manager.overwrite_impute = None
        self.manager.overwrite_model = None
        self.manager.cadd_version = None
        self.manager.grch_build = None

    def test_unit_preprocessing_file(self):
        """
        Unit test for the preprocessor to see if the preprocessor works just the file header information.
        """
        print('Preprocessing (unit) (file)')
        self.main.preprocess(loaded_cadd_data=self.main.impute(loaded_cadd_data=self.main.load_file()), train=False)

    def test_unit_preprocessing_config(self):
        """
        Unit test for the preprocessor to see if the preprocessor works with config variables.
        """
        print('Preprocessing (unit) (config)')
        self.main.cla_cadd_version = self.cadd_build
        self.main.cla_genome_build = self.grch_build
        self.main.preprocess(loaded_cadd_data=self.main.impute(loaded_cadd_data=self.main.load_file()), train=False)

    def test_unit_preprocessing_overwrite(self):
        """
        Unit test for the preprocessor to see if the preprocessor works with the config overwrite variables.
        """
        print('Preprocessing (unit) (overwrite)')
        self.manager.overwrite_impute = self.impute_overwrite
        self.manager.overwrite_model = self.model_overwrite
        self.main.preprocess(loaded_cadd_data=self.main.impute(loaded_cadd_data=self.main.load_file()), train=False)

    def test_component_preprocessing(self):
        """
        component test for preprocessing. All columns within the CADD features should be processed. Furthermore,
        within all processed columns, there should not be 1 or more column that is still considered categorical.
        """
        print('Preprocessing (component)')
        imputed_data = self.main.impute(loaded_cadd_data=self.main.load_file())
        preprocessor, processed_file = self.main.preprocess(loaded_cadd_data=imputed_data, train=False)
        model_features = preprocessor.get_model_features()
        processed_columns = processed_file.columns
        for feature in model_features:
            # Check if all model features are present before predicting
            self.assertIn(feature, processed_columns)
        # Check if none of the processed columns can be marked as categorical
        self.assertEqual(len(processed_file[model_features].select_dtypes(include=["O"]).columns), 0)

    def test_component_preprocessing_train(self):
        """
        Component test for the preprocessing part with train=True.
        """
        print('Preprocessing (train) (component)')
        self.manager.overwrite_impute = self.impute_overwrite
        loaded_file = self.main.load_file()
        imputed_file = self.main.impute(loaded_cadd_data=loaded_file)
        preprocessor, preprocessed_file = self.main.preprocess(loaded_cadd_data=imputed_file, train=True)

        # Since the init states that the model features are None by default, test if it is still None.
        self.assertIsNone(preprocessor.get_model_features())

        # Test if all columns matching, or starting with features within the imputing file are not classified objects.
        impute_features = self.manager.cadd_features
        processed_columns = preprocessed_file.columns
        present_features = 1  # Should be one, since the for loop quits before it can finish the last add_one
        test_features = []
        add_one = False
        for feature in impute_features:
            if add_one:
                present_features += 1
            add_one = False
            for processed_feature in processed_columns:
                if processed_feature.startswith(feature):
                    add_one = True
                    test_features.append(processed_feature)
        self.assertEqual(len(impute_features), present_features)  # Test if all impute features are present
        # Test if no columns are still objects.
        self.assertEqual(len(preprocessed_file[test_features].select_dtypes(include=["O"]).columns), 0)


if __name__ == '__main__':
    unittest.main()
