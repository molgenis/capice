import os
import unittest
import warnings

from src.main import Main
from src.global_manager import CapiceManager
from src.utilities.utilities import get_project_root_dir

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
        setup_class()

        # Initialize global manager and setting global variables
        cls.manager = CapiceManager()
        cls.manager.disable_logfile = True
        cls.manager.critical_logging_only = True
        cls.manager.verbose = False

        # Initialize main of prediction
        cls.main = Main(__program__=__program__,
                        __version__=__version__,
                        __author__=__author__,
                        input_loc=None,
                        output_loc=None,
                        cadd_build=None,
                        genome_build=None)

        # Defining input location
        cls.input_directory = os.path.join(get_project_root_dir(), 'CAPICE_example')

        # Dictionary specific to preprocessing and predict, usable files and their overwrite argument
        cls.processing_files_overwrite = {
            'test_cadd14_grch37_annotated.tsv.gz':
                'CAPICE using XGBoost 1.1.1, CADD 1.4 and genome build 37.'
        }
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
        self.main = Main(
            __program__=__program__,
            __version__=__version__,
            __author__=__author__,
            input_loc=None,
            output_loc=None,
            cadd_build=None,
            genome_build=None
        )
        self.manager.cadd_version = None
        self.manager.grch_build = None
        self.manager.overwrite_impute = False
        self.manager.overwrite_model = False
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

    def test_unit_imputation(self):
        """
        Unit test for imputation to be called with file CADD & GRCh arguments, CLA arguments and the overwrite argument.
        """
        print('Imputing (unit)')
        imputable_files = {
            'test_cadd14_grch37_annotated.tsv.gz':
                {
                    'cadd': 1.4,
                    'grch': 37,
                    'overwrite': 'CADD 1.4, GRCh build 37'
                }
        }
        types_input = ['CLA', 'file', 'overwrite']
        for file, items in imputable_files.items():
            print('Testing : {}'.format(file))
            input_loc = os.path.join(self.input_directory, file)
            for type_input in types_input:
                print('For type input: {}'.format(type_input))
                if type_input == 'CLA':
                    capice_main = Main(__program__=__program__,
                                       __version__=__version__,
                                       __author__=__author__,
                                       input_loc=input_loc,
                                       output_loc=None,
                                       cadd_build=imputable_files[file]['cadd'],
                                       genome_build=imputable_files[file]['grch']
                                       )
                    loaded_file = capice_main.load_file()
                    capice_main.impute(loaded_cadd_data=loaded_file)
                elif type_input == 'file':
                    self.main.infile = input_loc
                    loaded_file = self.main.load_file()
                    self.main.impute(loaded_cadd_data=loaded_file)
                else:
                    self.manager.overwrite_impute = imputable_files[file]['overwrite']
                    self.main.infile = input_loc
                    loaded_file = self.main.load_file()
                    self.main.impute(loaded_cadd_data=loaded_file)

    def test_component_imputation(self):
        """
        component test for the imputer to see if there are any gaps after the imputer has processed the data.
        """
        print('Imputing (component)')
        imputable_files = {'test_cadd14_grch37_annotated.tsv.gz': 'CADD 1.4, GRCh build 37'}
        for file, overwrite in imputable_files.items():
            print('For file: {}'.format(file))
            curr_file = os.path.join(self.input_directory, file)
            self.main.infile = curr_file
            self.manager.overwrite_impute = overwrite
            file = self.main.load_file()
            imputed_file = self.main.impute(loaded_cadd_data=file)
            imputed_columns = self.manager.cadd_features
            self.assertFalse(imputed_file[imputed_columns].isnull().values.any())

    def test_unit_preprocessing(self):
        """
        Unit test for the preprocessor to see if the preprocessor works with the CLA and file CADD version and
        GRCh build, as well as the overwrite argument.
        """
        print('Preprocessing (unit)')
        preprocessable_files = {
            'test_cadd14_grch37_annotated.tsv.gz': {
                'cadd': 1.4,
                'grch': 37,
                'overwrite': 'CAPICE using XGBoost 1.1.1, CADD 1.4 and genome build 37.'
            }
        }
        types_input = ['CLA', 'file', 'overwrite']
        for file, items in preprocessable_files.items():
            print('Testing: {}'.format(file))
            input_loc = os.path.join(self.input_directory, file)
            for type_input in types_input:
                print('For type of input: {}'.format(type_input))
                self.main.infile = input_loc
                if type_input == 'file':
                    file = self.main.load_file()
                    imputed_file = self.main.impute(loaded_cadd_data=file)
                    self.main.preprocess(loaded_cadd_data=imputed_file, train=False)
                    self.tearDown()
                elif type_input == 'CLA':
                    self.main.cla_cadd_version = preprocessable_files[file]['cadd']
                    self.main.cla_genome_build = preprocessable_files[file]['grch']
                    file = self.main.load_file()
                    imputed_file = self.main.impute(loaded_cadd_data=file)
                    self.main.preprocess(loaded_cadd_data=imputed_file, train=False)
                    self.tearDown()
                else:
                    self.manager.overwrite_model = items['overwrite']
                    file = self.main.load_file()
                    imputed_file = self.main.impute(loaded_cadd_data=file)
                    self.main.preprocess(loaded_cadd_data=imputed_file, train=False)
                    self.tearDown()

    def prepare_upon_preprocessing(self, model, file, preprocess=True, train=False):
        input_file = os.path.join(self.input_directory, file)
        self.manager.overwrite_model = model
        self.main.infile = input_file
        file = self.main.load_file()
        imputed_file = self.main.impute(loaded_cadd_data=file)
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
        for file, overwrite in self.processing_files_overwrite.items():
            preprocessor, processed_file = self.prepare_upon_preprocessing(model=overwrite, file=file)
            model_features = preprocessor.get_model_features()
            for feature in model_features:
                # Check if all model features are present before predicting
                self.assertIn(feature, processed_file.columns)
            # Check if none of the processed columns can be marked as categorical
            self.assertEqual(len(processed_file[model_features].select_dtypes(include=["O"]).columns), 0)

    def test_unit_prediction(self):
        print('Prediction (unit)')
        for file, overwrite in self.processing_files_overwrite.items():
            preprocessing_instance, processed_file = self.prepare_upon_preprocessing(model=overwrite, file=file)
            self.main.predict(loaded_cadd_data=processed_file, preprocessing_instance=preprocessing_instance)

    def test_component_prediction(self):
        print('Prediction (component)')
        for file, overwrite in self.processing_files_overwrite.items():
            preprocessing_instance, processed_file = self.prepare_upon_preprocessing(model=overwrite, file=file)
            prediction = self.main.predict(loaded_cadd_data=processed_file,
                                           preprocessing_instance=preprocessing_instance)
            # Combined sum of the prediction score should be higher than 0
            self.assertGreater(prediction['probabilities'].sum(), 0)


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
