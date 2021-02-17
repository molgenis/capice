import unittest
import warnings
import os

from src.main import Main
from src.global_manager import CapiceManager
from src.utilities.utilities import get_project_root_dir

__program__ = 'CAPICE prediction testing'
__version__ = 1.0
__author__ = 'R.J. Sietsma'


class Test(unittest.TestCase):
    """
    Testing module for both CAPICE and CAPICE predictions
    """

    @classmethod
    def setUpClass(cls):
        """
        Class to set up temporary directories for output files.
        :return:
        """
        print("Performing setting up")
        output_dir = os.path.join('.', 'testing_ouput')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        cls.manager = CapiceManager()
        cls.manager.disable_logfile(disable_logfile=True)
        cls.manager.set_critical_logs_only(critical_logs_only=True)
        cls.main = Main(__program__=__program__,
                        __version__=__version__,
                        __author__=__author__,
                        input_loc=None,
                        output_loc=None,
                        cadd_build=None,
                        genome_build=None)
        cls.input_examples = os.path.join(get_project_root_dir(), 'CAPICE_example')
        print('Set up complete, testing cases.')

    @classmethod
    def tearDownClass(cls):
        """
        Class method to tear down any directories and/ or files made during testing.
        """
        print("Performing teardown")
        output_dir = os.path.join('.', 'testing_ouput')
        if os.path.exists(output_dir):
            files_in_output = os.listdir(output_dir)
            if len(files_in_output) > 0:
                for path in files_in_output:
                    if os.path.isdir(path):
                        warnings.warn('Could not delete {} since it is a directory. Please remove it manually.'.format(
                            path
                        ))
                    else:
                        os.remove(path)
        try:
            os.rmdir(output_dir)
        except OSError:
            warnings.warn('Could not remove {}, please remove manually.'.format(output_dir))

    def setUp(self):
        """
        Class to set up variables or directories before each and every test case.
        """
        print('Testing case:')

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
            full_path_to_load_files.append(os.path.join(self.input_examples, file))
        for file in full_path_to_load_files:
            self.main.infile = file
            self.main.load_file()

    def test_integration_loadfile(self):
        """
        Integration testing class for loading in files, whenever they meet at least desired dimensions.
        """
        files_and_shapes = {
            'test_cadd14_grch37_annotated.tsv.gz': {'shape': (20, 107), 'cadd': 1.4, 'genome_build': 37},
            'test_cadd14_grch38_annotated.tsv.gz': {'shape': (6, 125), 'cadd': 1.4, 'genome_build': 38},
            'test_cadd16_grch37_annotated.tsv.gz': {'shape': (21, 116), 'cadd': 1.6, 'genome_build': 37},
            'test_cadd16_grch38_annotated.tsv.gz': {'shape': (6, 134), 'cadd': 1.6, 'genome_build': 38}}
        for curr_test_file, value in files_and_shapes.items():
            print('Load file (integration) for file {}'.format(curr_test_file))
            required_shape = value['shape']
            required_cadd_version = value['cadd']
            required_genome_build = value['genome_build']
            self.main.infile = os.path.join(self.input_examples, curr_test_file)
            file = self.main.load_file()
            self.assertEqual(file.shape, required_shape)
            self.assertEqual(self.manager.get_cadd_version(), required_cadd_version)
            self.assertEqual(self.manager.get_grch_build(), required_genome_build)

    def test_unit_imputation(self):
        print('Imputing (unit)')

        pass

    def test_integration_imputation(self):
        print('Imputing (integration)')
        pass

    def test_unit_preprocessing(self):
        print('Preprocessing (unit)')
        pass

    def test_integration_preprocessing(self):
        print('Preprocessing (integration)')
        pass

    def test_unit_prediction(self):
        print('Prediction (unit)')
        pass

    def test_integration_prediction(self):
        print('Prediction (integration)')
        pass

    # Could add another integration test for the export dataset


if __name__ == '__main__':
    unittest.main()
