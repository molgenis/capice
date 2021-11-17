import os
import unittest

from src.main.python.utilities.utilities import get_project_root_dir
from src.test.python.test_templates import set_up_manager_and_loc, teardown,\
    set_up_predict


class TestFileParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.manager, output_loc = set_up_manager_and_loc()
        input_file = os.path.join(get_project_root_dir(), 'CAPICE_example', 'CAPICE_input.tsv.gz')
        cls.main = set_up_predict()
        cls.main.infile = input_file

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        teardown()

    def setUp(self):
        print('Testing case:')

    def test_unit_loadfile(self):
        """
        Testing class for loading in files.
        """
        print('Load file (unit)')
        self.main._load_file()

    def test_component_loadfile(self):
        """
        component testing class for loading in files, whenever they meet at
        least desired dimensions.
        """
        required_shape = (20, 22)
        file = self.main._load_file()
        self.assertEqual(file.shape, required_shape)


if __name__ == '__main__':
    unittest.main()
