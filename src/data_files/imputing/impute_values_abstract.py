from abc import ABCMeta, abstractmethod
from src.logger import Logger


class TemplateImputeValues(metaclass=ABCMeta):
    """
    Abstract template class for new imputing files.
    """
    def __init__(self, name, usable, cadd_version, grch_build):
        self.log = Logger().get_logger()
        self.get_name = name
        self.is_usable = usable
        self.get_supported_cadd_version = cadd_version
        self.get_supported_grch_build = grch_build

    @property
    def get_name(self):
        return self._name

    @get_name.setter
    def get_name(self, value='Template'):
        if not isinstance(value, str):
            error_message = 'Expected a string usable variable, but got {}.'.format(type(value))
            self.log.critical(error_message)
            raise TypeError(error_message)
        self._name = value

    @property
    def is_usable(self):
        return self._usable

    @is_usable.setter
    def is_usable(self, value=False):
        if not isinstance(value, bool):
            error_message = 'Expected a boolean usable variable, but got {}.'.format(type(value))
            self.log.critical(error_message)
            raise TypeError(error_message)
        self._usable = value

    @property
    def get_supported_cadd_version(self):
        return self._cadd_version

    @get_supported_cadd_version.setter
    def get_supported_cadd_version(self, value):
        if not isinstance(value, float):
            error_message = 'Expected a float cadd version, but got: {}.'.format(type(value))
            self.log.critical(error_message)
            raise TypeError(error_message)
        self._cadd_version = value

    @property
    def get_supported_grch_build(self):
        return self._grch_build

    @get_supported_grch_build.setter
    def get_supported_grch_build(self, value):
        if not isinstance(value, int):
            error_message = 'Expected a integer usable variable, but got {}.'.format(type(value))
            self.log.critical(error_message)
            raise TypeError(error_message)
        self._grch_build = value

    @staticmethod
    @abstractmethod
    def _cadd_features():
        """
        Abstract template function to define a list of all CADD features that are of interest of a particular
        CADD version and GRCh build.
        :return: list
        """
        return []

    @staticmethod
    @abstractmethod
    def _impute_values():
        """
        Abstract template function to define a dictionary of all CADD features defined in _cadd_features() and their
        default (/impute) values.
        :return: dictionary
        """
        return {}

    def get_cadd_features(self):
        """
        Function for the modules that use the impute files to get the actual CADD features.
        :return: list
        """
        return self._cadd_features()

    def get_impute_values(self):
        """
        Function for the modules that use the impute files to get the actual impute and default values.
        :return: dictionary
        """
        return self._impute_values()
