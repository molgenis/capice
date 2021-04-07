from abc import ABCMeta, abstractmethod
from src.main.python.core.logger import Logger


class TemplateImputeValues(metaclass=ABCMeta):
    """
    Abstract template class for new imputing files.
    """
    def __init__(self, name, usable, cadd_version, grch_build):
        self.log = Logger().logger
        self.name = name
        self.usable = usable
        self.supported_cadd_version = cadd_version
        self.supported_grch_build = grch_build

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value='Template'):
        if not isinstance(value, str):
            error_message = 'Expected a string usable variable, but got {}.'.format(type(value))
            self.log.critical(error_message)
            raise TypeError(error_message)
        self._name = value

    @property
    def usable(self):
        return self._usable

    @usable.setter
    def usable(self, value=False):
        if not isinstance(value, bool):
            error_message = 'Expected a boolean usable variable, but got {}.'.format(type(value))
            self.log.critical(error_message)
            raise TypeError(error_message)
        self._usable = value

    @property
    def supported_cadd_version(self):
        return self._cadd_version

    @supported_cadd_version.setter
    def supported_cadd_version(self, value):
        if not isinstance(value, float):
            error_message = 'Expected a float cadd version, but got: {}.'.format(type(value))
            self.log.critical(error_message)
            raise TypeError(error_message)
        self._cadd_version = value

    @property
    def supported_grch_build(self):
        return self._grch_build

    @supported_grch_build.setter
    def supported_grch_build(self, value):
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

    @property
    def cadd_features(self):
        """
        Property cadd_features getter. Get the CADD features as defined within an impute file.

        :return: list
        """
        return self._cadd_features()

    @property
    def impute_values(self):
        """
        Property impute_values getter. Get the default / impute values as defined within an impute file.

        :return: dict
        """
        return self._impute_values()
