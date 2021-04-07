import unittest
import os
from datetime import datetime
import pickle

from src.main_train import Train
from src.main_capice import Main
from src.main.python.core.global_manager import CapiceManager
from src.main.python.resources.utilities.utilities import get_project_root_dir
from test_global import setup_class, teardown_class, __program__, __version__, __author__


class Test(unittest.TestCase):
    """
    Testing module for both creating new CAPICE like models
    """
    @classmethod
    def setUpClass(cls):

        cls.output_dir = setup_class()

        cls.manager = CapiceManager()
        cls.manager.now = datetime.now()
        cls.manager.disable_logfile = True
        cls.manager.critical_logging_only = True
        cls.manager.verbose = False

        test_file = 'train_dataset.tsv.gz'  # Replace with the name of the file you want to test

        # Replace with the version that you want to use and is supported in the imputing files
        impute_overwrite = "CADD 1.4, GRCh build 37"

        cls.input_loc = os.path.join(get_project_root_dir(), 'CAPICE_example')
        input_file = os.path.join(cls.input_loc, test_file)

        cls.manager.overwrite_impute = impute_overwrite

        cls.main = Train(__program__=__program__,
                         __version__=__version__,
                         __author__=__author__,
                         input_loc=input_file,
                         output_loc=cls.output_dir,
                         balance=False,  # Do need to test
                         default=False,  # Do need to test
                         specified_default=False,  # Do need to test
                         split=False,  # Do need to test
                         early_exit=False,
                         train_test_size=0.2  # Do need to test
                         )

        cls.processing_pipeline = Main(
            __program__=__program__,
            __version__=__version__,
            __author__=__author__,
            input_loc=input_file,
            output_loc=None,
            genome_build=None,
            cadd_build=None
        )

        print('Set up complete, testing cases.')

    @classmethod
    def tearDownClass(cls):
        teardown_class()

    def setUp(self):
        print('----------------------------------------------------------------------')
        print('Performing test:')

    def tearDown(self):
        print('Resetting arguments.')
        self.main.defaults = {}
        self.main.default = False
        self.main.specified_default = False
        print('----------------------------------------------------------------------')

    def test_integration_training(self):
        print('Training (integration)\n')
        self.main._integration_test = True
        self.main.main()
        output_filename = "randomized_search_cv_" + self.manager.now.strftime("%H%M%S%f_%d%m%Y") + '.pickle.dat'
        output_loc = os.path.join(self.output_dir, output_filename)
        with open(output_loc, 'rb') as model_dat:
            model = pickle.load(model_dat)
        class_used = str(model.__class__).split("'")[1]
        self.assertEqual('sklearn.model_selection._search.RandomizedSearchCV', class_used)
        best_model = str(model.best_estimator_.__class__).split("'")[1]
        self.assertEqual('xgboost.sklearn.XGBClassifier', best_model)

    def test_component_preprocessing(self):
        print('Preprocessing (train) (component)')
        loaded_file = self.processing_pipeline.load_file()
        imputed_file = self.processing_pipeline.impute(loaded_cadd_data=loaded_file)
        preprocessor, preprocessed_file = self.processing_pipeline.preprocess(loaded_cadd_data=imputed_file, train=True)

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

    def test_unit_split(self):
        print('Split (unit)')
        input_file = self.processing_pipeline.load_file()
        self.main.split_data(dataset=input_file, test_size=0.2)

    def test_component_split(self):
        print('Split (component)')
        input_file = self.processing_pipeline.load_file()
        train, test = self.main.split_data(dataset=input_file, test_size=0.2)
        total_size = input_file.shape[0]
        self.assertAlmostEqual(train.shape[0], total_size*0.8)
        self.assertAlmostEqual(test.shape[0], total_size*0.2)
        self.assertEqual(train.shape[0] + test.shape[0], total_size)

    def test_unit_load_defaults(self):
        print('Load_defaults (unit)')
        # Hardcoded hyper parameters
        self.main.load_defaults()
        # JSON encoded hyper parameters
        self.main.specified_default = os.path.join(self.input_loc, 'specified_defaults.json')
        self.main.load_defaults()

    def test_component_load_defaults(self):
        print('Load_defaults (component)')

        # Check the default default hyper parameters
        self.main.load_defaults()
        defaults = self.main.defaults
        self.assertEqual(defaults['learning_rate'], 0.10495845238185281)
        self.assertEqual(defaults['max_depth'], 422)
        self.assertEqual(defaults['n_estimators'], 15)

        # Check the loaded default hyper parameters
        self.main.specified_default = os.path.join(self.input_loc, 'specified_defaults.json')
        self.main.load_defaults()
        defaults = self.main.defaults
        self.assertEqual(defaults['learning_rate'], 0.5)
        self.assertEqual(defaults['max_depth'], 10)
        self.assertEqual(defaults['n_estimators'], 10)

    def test_unit_balancing(self):
        print('Balancing (unit)')
        file = self.processing_pipeline.load_file()
        self.main.process_balance_in_the_force(dataset=file)

    def test_component_balancing(self):
        print('Balancing (component)')
        file = self.processing_pipeline.load_file()
        balanced_file = self.main.process_balance_in_the_force(dataset=file)
        n_zero = balanced_file[balanced_file['binarized_label'] == 0].shape[0]
        n_one = balanced_file[balanced_file['binarized_label'] == 1].shape[0]
        self.assertEqual(n_zero, n_one)


if __name__ == '__main__':
    unittest.main()
