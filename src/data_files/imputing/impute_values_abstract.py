from abc import ABCMeta, abstractmethod


class TemplateImputeValues(metaclass=ABCMeta):
    def __init__(self):
        self.required_version = None
        self.required_build = None
        self.optional_feats = ['#Chrom', 'Pos', 'FeatureID']

    @staticmethod
    def get_name():
        return 'Template'

    def version_check(self, argument_version: float):
        """
        Function to check if the version given corresponds with this class's required version
        :param argument_version: float, the command line or file given CADD version
        :return: bool, true if match
        """
        if argument_version == self.required_version:
            return True
        else:
            return False

    def build_check(self, argument_build: float):
        """
        Function to check if the GRCh build given corresponds with this class's required build
        :param argument_build: int, the command line or file given GRCh build
        :return: bool, true if match
        """
        if argument_build == self.required_build:
            return True
        else:
            return False

    @staticmethod
    def _cadd_features():
        return []

    @staticmethod
    def _impute_values():
        return {}

    def get_cadd_features(self):
        for feature in self.optional_feats:
            if feature not in self._cadd_features():
                self._cadd_features().append(feature)
        return self._cadd_features()

    def get_impute_values(self):
        return self._impute_values()
