import os
import unittest
import pandas as pd
from src.main_capice import Main
from src.test.python.test_templates import set_up_manager_and_loc, teardown
from src.main.python.core.config_reader import ConfigReader
from src.main.python.resources.utilities.utilities import get_project_root_dir

__program__ = 'Main NonTrain test'
__version__ = 'testing'
__author__ = 'R.J. Sietsma'


class TestMainNonTrain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        manager, cls.output_dir = set_up_manager_and_loc()
        manager.output_filename = os.path.join(cls.output_dir, 'test_output.txt')
        ConfigReader().parse()

    @classmethod
    def tearDownClass(cls):
        print('Performing teardown.')
        teardown()

    def setUp(self):
        print('Performing test:')

    def test_integration_main_nontrain(self):
        print('Main no-train (integration)')
        infile = os.path.join(get_project_root_dir(), 'CAPICE_example', 'test_cadd14_grch37_annotated.tsv.gz')
        main = Main(__program__=__program__,
                    __version__=__version__,
                    __author__=__author__,
                    input_loc=infile,
                    output_loc=self.output_dir)
        main.run()
        prediction_output = pd.read_csv(os.path.join(self.output_dir, 'test_output.txt'), sep='\t')
        self.assertEqual(prediction_output.shape, (20, 7))


if __name__ == '__main__':
    unittest.main()
