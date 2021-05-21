import os
import time
import unittest
from src.main.python.resources.utilities.utilities import get_project_root_dir
from src.test.python.test_templates import set_up_manager_and_loc, teardown, set_up_main


class TestFileParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.manager, output_loc = set_up_manager_and_loc()
        input_file = os.path.join(get_project_root_dir(), 'CAPICE_example', 'test_cadd14_grch37_annotated.tsv.gz')
        cls.main = set_up_main()
        cls.main.infile = input_file

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        teardown()

    def setUp(self):
        print('Testing case:')

    def tearDown(self):
        print('Resetting arguments.')
        self.manager.cadd_version = None
        self.manager.grch_build = None
        print('Arguments reset.')

    def test_unit_loadfile(self):
        """
        Testing class for loading in files.
        """
        print('Load file (unit)')
        self.main.load_file()

    def test_component_loadfile(self):
        """
        component testing class for loading in files, whenever they meet at least desired dimensions.
        """
        required_shape = (20, 107)
        required_cadd_version = 1.4
        required_genome_build = 37
        file = self.main.load_file()
        self.assertEqual(file.shape, required_shape)
        self.assertEqual(self.manager.cadd_version, required_cadd_version)
        self.assertEqual(self.manager.grch_build, required_genome_build)


if __name__ == '__main__':
    unittest.main()
