from configparser import ConfigParser
from src.main.python.resources.utilities.utilities import get_project_root_dir
from src.main.python.resources.enums.sections import Sections
import os


class ConfigReader:
    class __ConfigReader:
        def __init__(self):
            self.config = ConfigParser()
            self.defaults = None
            self.overwrites = None
            self.misc = None
            self.datafiles = None
            self.train = None
            self.error = 'ERROR'

        def parse(self):
            self._parse()
            self._check_all_sections_present()
            self.defaults = self.config[Sections.DEFAULTS.value]
            self.overwrites = self.config[Sections.OVERWRITES.value]
            self.datafiles = self.config[Sections.DATAFILES.value]
            self.misc = self.config[Sections.MISC.value]
            self.train = self.config[Sections.TRAINING.value]

        def _parse(self):
            self.config.read(os.path.join(get_project_root_dir(), 'config.cfg'))

        def get_default_value(self, key):
            key = key.lower()
            value = self.defaults.get(key, fallback=self.error)
            self._check_value_has_error(value=value, keysearch=key, section='DEFAULTS')
            if key == 'genomebuild':
                value = self._check_value_default(value=value, else_type=int)
            elif key == 'caddversion':
                value = self._check_value_default(value=value, else_type=float)

            if key == 'logfilelocation':
                value = self._check_value_default(value=value, else_type=str)
            return value

        def get_overwrite_value(self, key):
            key = key.lower()
            value = self.overwrites.get(key, fallback=self.error)
            self._check_value_has_error(value=value, keysearch=key, section='OVERWRITES')
            value = self._check_value_default(value=value, else_type=str)
            return value

        def get_datafiles_value(self, key):
            key = key.lower()
            value = self.datafiles.get(key, fallback=self.error)
            self._check_value_has_error(value=value, keysearch=key, section='CADD')
            value = self._check_value_default(value=value, else_type=str)
            return value

        def get_misc_value(self, key):
            key = key.lower()
            boolean = ['enablelogfile']
            if key in boolean:
                value = self.misc.getboolean(key, fallback=self.error)
            else:
                value = self.misc.get(key, fallback=self.error)
            self._check_value_has_error(value=value, keysearch=key, section='MISC')
            return value

        def get_train_value(self, key):
            key = key.lower()
            boolean = ['makebalanced', 'earlyexit', 'default']
            float_values = ['split', 'traintestsize']
            if key in boolean:
                value = self.train.getboolean(key, fallback=self.error)
            elif key in float_values:
                value = self.train.getfloat(key, fallback=self.error)
            else:
                value = self.train.get(key, fallback=self.error)
            self._check_value_has_error(value=value, keysearch=key, section='TRAINING')
            value = self._check_value_default(value=value, else_type=str)
            return value

        def _check_value_has_error(self, value, keysearch, section):
            if value == self.error:
                self._raise_key_not_found(section=section, keysearch=keysearch)

        def _check_all_sections_present(self):
            should_be_present = ['DEFAULTS', 'OVERWRITES', 'DATAFILES', 'MISC', 'TRAINING']
            for section in should_be_present:
                if section not in self.config.sections():
                    raise KeyError('Unable to locate {} in config file.'.format(section))

        @staticmethod
        def _check_value_default(value, else_type):
            default = 'missing'
            none_default = 'output'
            if isinstance(value, str):
                if value.lower() == default:
                    value = False
                elif value.lower() == none_default:
                    value = None
                else:
                    value = else_type(value)
            return value

        def _raise_key_not_found(self, section, keysearch):
            raise KeyError('Not able to get request {} in section {}.'.format(keysearch, section))

    instance = None

    def parse(self):
        """
        Function to start parsing the config file to the singleton class
        """
        pass

    def get_default_value(self, key):
        """
        Function to get a value from the DEFAULTS section of the config.

        key: str
        """
        pass

    def get_overwrite_value(self, key):
        """
        Function to get a value from the OVERWRITES section of the config.

        key: str
        """
        pass

    def get_misc_value(self, key):
        """
        Function to get a value from the MISC section of the config.

        key: str
        """
        pass

    def get_cadd_value(self, key):
        """
        Function to get a value from the CADD section of the config.

        key: str
        """
        pass

    def get_train_value(self, key):
        """
        Function to get a value from the TRAINING section of the config.

        key: str
        """
        pass

    def __new__(cls):
        """
        Class method to set CapiceManager instance
        :return: instance
        """
        if not ConfigReader.instance:
            ConfigReader.instance = ConfigReader.__ConfigReader()
        return ConfigReader.instance

    def __init__(self):
        """
        __init__ method to set instance to CapiceManager.__CapiceManager()
        """
        if not ConfigReader.instance:
            ConfigReader.instance = ConfigReader.__ConfigReader()

    def __getattr__(self, name):
        """
        Method to return the value of the named attribute of name
        :param name: str
        :return: str
        """
        return getattr(self.instance, name)
