import unittest

from src.test.python.test_templates import set_up_impute_preprocess, teardown


class TestPreprocessing(unittest.TestCase):
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

    def test_unit_preprocessing_file(self):
        """
        Unit test for the preprocessor to see if the preprocessor works just
        the file header information.
        """
        print('Preprocessing (unit) (file)')
        self.main.preprocess(
            loaded_data=self.main.impute(
                loaded_data=self.main.process(
                    self.main._load_file()
                ), impute_values=self.model.impute_values
            ), model_features=self.model.get_booster().feature_names
        )

    def test_component_preprocessing(self):
        """
        component test for preprocessing. All columns within the CADD
        features should be processed. Furthermore,
        within all processed columns,
        there should not be 1 or more column that is still
        considered categorical.
        """
        print('Preprocessing (component)')
        processed_file = self.main.preprocess(
            self.main.impute(
                self.main.process(
                    self.main._load_file()
                ), impute_values=self.model.impute_values
            ), model_features=self.model.get_booster().feature_names
        )
        model_features = self.model.get_booster().feature_names
        processed_columns = processed_file.columns
        for feature in model_features:
            # Check if all model features are present before predicting
            self.assertIn(feature, processed_columns)
        # Check if none of the processed columns can be marked as categorical
        self.assertEqual(
            len(processed_file[model_features].select_dtypes(include=["O"]).columns),
            0
        )

    def test_component_preprocessing_train(self):
        """
        Component test for the preprocessing part with train=True.
        """
        print('Preprocessing (train) (component)')
        preprocessed_file = self.main.preprocess(
            self.main.impute(
                self.main.process(
                    self.main._load_file()
                ), impute_values=self.model.impute_values
            )
        )

        # Test if all columns matching,
        # or starting with features within the imputing
        # file are not classified objects.
        impute_features = self.model.impute_values.keys()
        processed_columns = preprocessed_file.columns
        present_features = 1
        # Should be one, since the for loop quits before
        # it can finish the last add_one
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
        # Test if all impute features are present
        self.assertEqual(len(impute_features), present_features)
        # Test if no columns are still objects.
        self.assertEqual(
            len(preprocessed_file[test_features].select_dtypes(include=["O"]).columns),
            0
        )


if __name__ == '__main__':
    unittest.main()
