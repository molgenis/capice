import unittest
from src.main.python.core.config_reader import ConfigReader
from src.main.python.core.global_manager import CapiceManager
from src.main.python.resources.utilities.utilities import get_project_root_dir
import os


class TestConfigReaderAlternativeLocation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        ConfigReader.instance = None
        cls.manager = CapiceManager()
        cls.config_loc = os.path.join(
            get_project_root_dir(),
            'CAPICE_example',
            'not_so_default.cfg'
        )
        print(cls.config_loc)
        cls.manager.config_loc = cls.config_loc
        cls.config = ConfigReader()
        cls.config.parse()

    @classmethod
    def tearDownClass(cls) -> None:
        print('Tearing down.')
        ConfigReader.instance = None
        CapiceManager.instance = None

    def setUp(self):
        print('Testing case:')

    def test_alternative_set(self):
        print('Alternative config location set')
        self.assertEqual(self.config.config_loc, self.config_loc)

    def test_alternative_config_loc(self):
        print('Alternative config location odd value')
        value = self.config.get_default_value(key='genomebuild')
        self.assertEqual(value, 20)


if __name__ == '__main__':
    unittest.main()
