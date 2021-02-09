from abc import ABCMeta, abstractmethod


class TemplateImputeValues(metaclass=ABCMeta):
    """
    Abstract template class for new imputing files.
    """

    @staticmethod
    @abstractmethod
    def get_name():
        """
        Function to define a name for an Imputing file. Can be used to match the --overwrite_impute_file command line
        argument.
        :return: string
        """
        return 'Template'

    @staticmethod
    @abstractmethod
    def is_usable():
        """
        Function to define if this class is usable or exists just as a template or for very specific goals where
        the imputing file is hardcoded.
        :return: boolean
        """
        return False

    @staticmethod
    @abstractmethod
    def get_supported_cadd_version():
        """
        Function to define the CADD version that the imputing file is designed for.
        :return: float
        """
        pass

    @staticmethod
    @abstractmethod
    def get_supported_grch_build():
        """
        Function to define the GRCh build that the imputing file is designed for.
        :return: integer
        """
        pass

    def version_check(self, argument_version: float):
        """
        Function to check if the version given corresponds with this class's required version
        :param argument_version: float, the command line or file given CADD version
        :return: bool, true if match
        """
        if argument_version == self.get_supported_cadd_version():
            return True
        else:
            return False

    def build_check(self, argument_build: float):
        """
        Function to check if the GRCh build given corresponds with this class's required build
        :param argument_build: int, the command line or file given GRCh build
        :return: bool, true if match
        """
        if argument_build == self.get_supported_grch_build():
            return True
        else:
            return False

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
