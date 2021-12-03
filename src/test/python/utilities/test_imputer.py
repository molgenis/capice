import unittest

from src.test.python.test_templates import set_up_impute_preprocess, teardown


class TestImputer(unittest.TestCase):
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

    def test_unit_imputation_file(self):
        """
        Unit test for imputation to be called with only the file header
        information.
        """
        print('Imputing (unit) (file)')
        self.main.impute(
            loaded_data=self.main.process(
                self.main._load_file()
            ), impute_values=self.model.impute_values
        )

    def test_component_imputation(self):
        """
        component test for the imputer to see if there are any gaps after the
        imputer has processed the data.
        """
        print('Imputing (component)')
        imputed_file = self.main.impute(
            loaded_data=self.main.process(
                self.main._load_file()
            ), impute_values=self.model.impute_values
        )
        self.assertFalse(imputed_file[self.model.impute_values.keys()].isnull().values.any())


if __name__ == '__main__':
    unittest.main()
