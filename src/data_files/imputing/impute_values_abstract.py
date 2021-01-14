from abc import ABCMeta, abstractmethod


class TemplateImputeValues(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_name():
        return 'Template'

    @staticmethod
    @abstractmethod
    def is_usable():
        return False

    @staticmethod
    @abstractmethod
    def get_supported_cadd_version():
        pass

    @staticmethod
    @abstractmethod
    def get_supported_grch_build():
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
        return []

    @staticmethod
    @abstractmethod
    def _impute_values():
        return {}

    def get_cadd_features(self):
        return self._cadd_features()

    def get_impute_values(self):
        return self._impute_values()
