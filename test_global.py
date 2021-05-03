import os
import unittest
import warnings
import pickle
import time
from datetime import datetime

from src.main_train import Train
from src.main.python.core.global_manager import CapiceManager
from src.main.python.core.config_reader import ConfigReader
from src.main.python.resources.utilities.utilities import get_project_root_dir

from src.main.python.core.input_checker import InputChecker

__program__ = 'CAPICE prediction testing'
__version__ = 1.0
__author__ = 'R.J. Sietsma'


class TestGlobal(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Class to set up temporary directories for output files.
        :return:
        """
        print("Performing setting up")

        # Training specific setup arguments
        cls.output = setup_class()
        cls.train_file = os.path.join(get_project_root_dir(), 'CAPICE_example', 'train_dataset.tsv.gz')

        # Defining input location
        cls.input_directory = os.path.join(get_project_root_dir(), 'CAPICE_example')

        # To be investigated file
        cls.input_file = os.path.join(cls.input_directory, 'test_cadd14_grch37_annotated.tsv.gz')
        cls.cadd_build = 1.4
        cls.grch_build = 37
        cls.impute_overwrite = 'CADD 1.4, GRCh build 37'
        cls.model_overwrite = 'CAPICE using XGBoost 0.72.1, CADD 1.4 and genome build 37.'

        # Initialize global manager and setting global variables
        cls.manager = CapiceManager()
        cls.manager.now = datetime.now()
        cls.manager.disable_logfile = True
        cls.manager.critical_logging_only = True
        cls.manager.verbose = False

        # Initialize config
        ConfigReader().parse()

        # Initialize main of prediction
        cls.main = Train(__program__=__program__,
                         __version__=__version__,
                         __author__=__author__,
                         input_loc=cls.input_file,
                         output_loc=cls.output)

        # Case specific testing
        cls.input_checker = InputChecker()

        print('Set up complete, testing cases.')

    @classmethod
    def tearDownClass(cls):
        teardown_class()

    def setUp(self):
        """
        Class to set up variables or directories before each and every test case.
        """
        print('----------------------------------------------------------------------')
        print('Testing case:')

    def tearDown(self):
        """
        Class to reset variables to their original state after every test case.
        """
        print('Resetting arguments')
        self.main.cla_cadd_version = False
        self.main.cla_genome_build = False
        self.main.infile = self.input_file
        self.manager.cadd_version = None
        self.manager.grch_build = None
        self.manager.overwrite_impute = False
        self.manager.overwrite_model = False

        # Training specific resets
        self.main.default = False
        self.main.balance = False
        self.main.specified_default = False
        self.main._integration_test = False

        # Case specific resets
        self.input_checker.output_filename = ''
        self.input_checker.output_directory = ''
        time.sleep(0.5)
        print('----------------------------------------------------------------------')

    def test_unit_loadfile(self):
        """
        Testing class for loading in files.
        """
        print('Load file (unit)')
        to_be_loaded_files = ['test_cadd14_grch38_annotated.tsv.gz',
                              'test_cadd14_grch37_annotated.tsv.gz',
                              'test_cadd16_grch38_annotated.tsv.gz',
                              'test_cadd16_grch37_annotated.tsv.gz']
        full_path_to_load_files = []
        for file in to_be_loaded_files:
            full_path_to_load_files.append(os.path.join(self.input_directory, file))
        for file in full_path_to_load_files:
            print('Testing {}'.format(file))
            self.main.infile = file
            self.main.load_file()

    def test_component_loadfile(self):
        """
        component testing class for loading in files, whenever they meet at least desired dimensions.
        """
        files_and_shapes = {
            'test_cadd14_grch37_annotated.tsv.gz': {'shape': (20, 107), 'cadd': 1.4, 'genome_build': 37},
            'test_cadd14_grch38_annotated.tsv.gz': {'shape': (6, 125), 'cadd': 1.4, 'genome_build': 38},
            'test_cadd16_grch37_annotated.tsv.gz': {'shape': (21, 116), 'cadd': 1.6, 'genome_build': 37},
            'test_cadd16_grch38_annotated.tsv.gz': {'shape': (6, 134), 'cadd': 1.6, 'genome_build': 38}}
        for curr_test_file, value in files_and_shapes.items():
            print('Load file (component) for file {}'.format(curr_test_file))
            required_shape = value['shape']
            required_cadd_version = value['cadd']
            required_genome_build = value['genome_build']
            self.main.infile = os.path.join(self.input_directory, curr_test_file)
            file = self.main.load_file()
            self.assertEqual(file.shape, required_shape)
            self.assertEqual(self.manager.cadd_version, required_cadd_version)
            self.assertEqual(self.manager.grch_build, required_genome_build)

    def test_unit_imputation_config(self):
        """
        Unit test for imputation to be called with config specific arguments.
        """
        print('Imputing (unit) (config)')
        self.main.cla_cadd_version = self.cadd_build
        self.main.cla_genome_build = self.grch_build
        self.main.impute(loaded_cadd_data=self.main.load_file())

    def test_unit_imputation_file(self):
        """
        Unit test for imputation to be called with only the file header information.
        """
        print('Imputing (unit) (file)')
        self.main.impute(loaded_cadd_data=self.main.load_file())

    def test_unit_imputation_overwrite(self):
        """
        Unit test for imputation to be called with only the overwrite config variable.
        """
        print('Imputing (unit) (overwrite)')
        self.manager.overwrite_impute = self.impute_overwrite
        self.main.impute(loaded_cadd_data=self.main.load_file())

    def test_component_imputation(self):
        """
        component test for the imputer to see if there are any gaps after the imputer has processed the data.
        """
        print('Imputing (component)')
        self.manager.overwrite_impute = self.impute_overwrite
        imputed_file = self.main.impute(loaded_cadd_data=self.main.load_file())
        imputed_columns = self.manager.cadd_features
        self.assertFalse(imputed_file[imputed_columns].isnull().values.any())

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

    def prepare_upon_preprocessing(self, model, preprocess=True, train=False):
        self.manager.overwrite_model = model
        imputed_file = self.main.impute(loaded_cadd_data=self.main.load_file())
        if preprocess:
            preprocessor, processed_file = self.main.preprocess(loaded_cadd_data=imputed_file,
                                                                train=train)
            return preprocessor, processed_file
        else:
            return None, imputed_file

    def test_component_preprocessing(self):
        """
        component test for preprocessing. All columns within the CADD features should be processed. Furthermore,
        within all processed columns, there should not be 1 or more column that is still considered categorical.
        """
        print('Preprocessing (component)')
        preprocessor, processed_file = self.prepare_upon_preprocessing(model=self.model_overwrite)
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

    def test_unit_prediction(self):
        """
        Unit test for the prediction part of CAPICE.
        """
        print('Prediction (unit)')
        preprocessing_instance, processed_file = self.prepare_upon_preprocessing(model=self.model_overwrite)
        self.main.predict(loaded_cadd_data=processed_file, preprocessing_instance=preprocessing_instance)

    def test_component_prediction(self):
        """
        Component test for prediction to see if the combined score of all is greater than 0.
        """
        print('Prediction (component)')
        preprocessing_instance, processed_file = self.prepare_upon_preprocessing(model=self.model_overwrite)
        prediction = self.main.predict(loaded_cadd_data=processed_file,
                                       preprocessing_instance=preprocessing_instance)
        # Combined sum of the prediction score should be higher than 0
        self.assertGreater(prediction['probabilities'].sum(), 0)

    def test_integration_training(self):
        """
        Integration test for the full training part of CAPICE. With check if the correct class is exported.
        """
        print('Training (integration)')
        self.main.infile = self.train_file
        self.manager.overwrite_impute = self.impute_overwrite
        self.main._integration_test = True
        self.main.run()
        output_filename = "randomized_search_cv_" + self.manager.now.strftime("%H%M%S%f_%d%m%Y") + '.pickle.dat'
        output_loc = os.path.join(self.output, output_filename)
        with open(output_loc, 'rb') as model_dat:
            model = pickle.load(model_dat)
        class_used = str(model.__class__).split("'")[1]
        self.assertEqual('sklearn.model_selection._search.RandomizedSearchCV', class_used)
        best_model = str(model.best_estimator_.__class__).split("'")[1]
        self.assertEqual('xgboost.sklearn.XGBClassifier', best_model)

    def test_unit_split(self):
        """
        Unit test to see if split works.
        """
        print('Split (unit)')
        self.main.infile = self.train_file
        self.manager.overwrite_impute = self.impute_overwrite
        input_file = self.main.load_file()
        self.main.split_data(dataset=input_file, test_size=0.2)

    def test_component_split(self):
        """
        Component test for split to see if the correct sizes of datasets are created.
        """
        print('Split (component)')
        self.main.infile = self.train_file
        self.manager.overwrite_impute = self.impute_overwrite
        input_file = self.main.load_file()
        train, test = self.main.split_data(dataset=input_file, test_size=0.2)
        total_size = input_file.shape[0]
        self.assertAlmostEqual(train.shape[0], total_size*0.8)
        self.assertAlmostEqual(test.shape[0], total_size*0.2)
        self.assertEqual(train.shape[0] + test.shape[0], total_size)

    def test_unit_load_defaults(self):
        """
        Unit test to see if the default hyper parameters can be loaded.
        """
        print('Load_defaults (unit)')
        self.main.load_defaults()

    def test_unit_load_specified_defaults(self):
        """
        Unit test to see if specified default hyper parameters can be loaded.
        """
        print('Load_specified_defaults (unit)')
        self.main.specified_default = os.path.join(self.input_directory, 'specified_defaults.json')
        self.main.load_defaults()

    def test_component_load_defaults(self):
        """
        Component test to see if default hyper parameters are correctly loaded according to expectation.
        """
        print('Load_defaults (component)')
        self.main.load_defaults()
        defaults = self.main.defaults
        self.assertEqual(defaults['learning_rate'], 0.10495845238185281)
        self.assertEqual(defaults['max_depth'], 422)
        self.assertEqual(defaults['n_estimators'], 15)

    def test_component_load_specified_defaults(self):
        """
        Component test to see if specified default hyper parameters are loaded correctly.
        """
        print('Load_specified_defaults (component)')
        self.main.specified_default = os.path.join(self.input_directory, 'specified_defaults.json')
        self.main.load_defaults()
        defaults = self.main.defaults
        self.assertEqual(defaults['learning_rate'], 0.5)
        self.assertEqual(defaults['max_depth'], 10)
        self.assertEqual(defaults['n_estimators'], 10)

    def test_unit_balancing(self):
        """
        Unit test for the balancing algorithm.
        """
        print('Balancing (unit)')
        self.main.infile = self.train_file
        self.manager.overwrite_impute = self.impute_overwrite
        self.main.process_balance_in_the_force(dataset=self.main.load_file())

    def test_component_balancing(self):
        """
        Component test for the balancing with test to see if the amount of benign and pathogenic variants are the same.
        """
        print('Balancing (component)')
        self.main.infile = self.train_file
        self.manager.overwrite_impute = self.impute_overwrite
        balanced_file = self.main.process_balance_in_the_force(dataset=self.main.load_file())
        n_zero = balanced_file[balanced_file['binarized_label'] == 0].shape[0]
        n_one = balanced_file[balanced_file['binarized_label'] == 1].shape[0]
        self.assertEqual(n_zero, n_one)

    def test_input_output_conversion_case1(self):
        """
        Test for the input checker if the correct input, output directory and output filename are set.
        Testing with only an input
        """
        print('Input output conversion (input only)')
        test_input = './CAPICE_example/test_cadd14_grch37_annotated.tsv.gz'
        test_output = None
        expected_output_filename = 'test_cadd14_grch37_annotated_capice.tsv.gz'
        expected_output_directory = './CAPICE_example'
        self.input_checker.check_input_output_directories(input_path=test_input, output_path=test_output)
        self.assertEqual(self.input_checker.get_output_filename(), expected_output_filename)
        self.assertEqual(self.input_checker.get_output_directory(), expected_output_directory)

    def test_input_output_conversion_case2(self):
        """
        Test for the input checker if the correct input, output directory and output filename are set.
        Testing with input and an output directory.
        """
        print('Input output conversion (input + output directory)')
        test_input = './CAPICE_example/test_cadd14_grch37_annotated.tsv.gz'
        test_output = './test_output'
        expected_output_filename = 'test_cadd14_grch37_annotated_capice.tsv.gz'
        expected_output_directory = './test_output'
        self.input_checker.check_input_output_directories(input_path=test_input, output_path=test_output)
        self.assertEqual(self.input_checker.get_output_filename(), expected_output_filename)
        self.assertEqual(self.input_checker.get_output_directory(), expected_output_directory)

    def test_input_output_conversion_case3(self):
        """
        Test for the input checker if the correct input, output directory and output filename are set.
        Testing with input, output directory AND filename.
        """
        print('Input output conversion (input + output directory + filename)')
        test_input = './CAPICE_example/test_cadd14_grch37_annotated.tsv.gz'
        test_output = './test_output/test.txt'
        # expected_output_filename = 'test.txt.gz'
        expected_output_filename = 'test.txt'  # Legacy support, if legacy is disabled can be removed.
        expected_output_directory = './test_output'
        self.input_checker.check_input_output_directories(input_path=test_input, output_path=test_output)
        self.assertEqual(self.input_checker.get_output_filename(), expected_output_filename)
        self.assertEqual(self.input_checker.get_output_directory(), expected_output_directory)


def setup_class():
    """
    Globally available method to create the output directory before anything happens
    """
    output_dir = os.path.join('.', 'testing_output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def teardown_class():
    """
    Class method to tear down any directories and/ or files made during testing.
    """
    print("Performing teardown")
    # Deleting output directory if it exists
    output_dir = os.path.join('.', 'testing_output')
    if os.path.exists(output_dir):
        # Checking for files within the output directory
        files_in_output = os.listdir(output_dir)
        if len(files_in_output) > 0:
            for path in files_in_output:
                path = os.path.join(output_dir, path)
                # Delete if path is file, else just throw a warning
                if os.path.isdir(path):
                    warnings.warn('Could not delete {} since it is a directory. Please remove it manually.'.format(
                        path
                    ))
                else:
                    os.remove(path)
    try:
        # Attempt to remove output directory
        os.rmdir(output_dir)
    except OSError:
        # Warn user if it can't be deleted manually
        warnings.warn('Could not remove {}, please remove manually.'.format(output_dir))


if __name__ == '__main__':
    unittest.main()
