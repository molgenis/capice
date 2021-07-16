from abc import ABCMeta, abstractmethod
from src.main.python.core.logger import Logger
from src.main.python.resources.utilities.utilities import get_project_root_dir
from src.main.python.resources.checkers.property_checker_logger import \
    PropertyCheckerLogger
import os
import json


class TemplateImputeValues(metaclass=ABCMeta):
    """
    Abstract template class for new imputing files.
    """

    def __init__(self, name, usable, vep_version, grch_build):
        self.log = Logger().logger
        self.property_checker = PropertyCheckerLogger()
        self.name = name
        self.usable = usable
        self.supported_vep_version = vep_version
        self.supported_grch_build = grch_build
        self.impute_data = self._get_impute_data()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value='Template'):
        self.property_checker.check_property(value=value, expected_type=str)
        self._name = value

    @property
    def usable(self):
        return self._usable

    @usable.setter
    def usable(self, value=False):
        self.property_checker.check_property(value=value, expected_type=bool)
        self._usable = value

    @property
    def supported_vep_version(self):
        return self._vep_version

    @supported_vep_version.setter
    def supported_vep_version(self, value):
        self.property_checker.check_property(value=value, expected_type=float)
        self._vep_version = value

    @property
    def supported_grch_build(self):
        return self._grch_build

    @supported_grch_build.setter
    def supported_grch_build(self, value):
        self.property_checker.check_property(value=value, expected_type=int)
        self._grch_build = value

    def _get_impute_data(self):
        with open(self._json_loc()) as json_file:
            json_data = json.load(json_file)
        return json_data

    def _json_loc(self):
        path = os.path.join(
            get_project_root_dir(),
            'src',
            'main',
            'python',
            'resources',
            'data_files',
            'json_data'
        )
        json_name = self._json_name()
        if json_name == 'none':
            error_message = 'Location of JSON must be specified!'
            self.log.critical(error_message)
            raise FileNotFoundError(error_message)
        return os.path.join(path, json_name)

    @staticmethod
    @abstractmethod
    def _json_name():
        """
        Abstract template function to define the location of where the imputing
        JSON is stored, containing the required columns for the input datafile.
        :return: path-like
        """
        return 'none'

    @property
    def annotation_features(self):
        """
        Property getter annotation_feature.
        Get the annotation features defined within the impute file.

        :return: list
        """
        return list(self.impute_data.keys())

    @property
    def impute_values(self):
        """
        Property impute_values getter. Get the default / impute values as
        defined within an impute file.

        :return: dict
        """
        return_dict = {}
        for key, value in self.impute_data.items():
            if value is not None:
                return_dict[key] = value
        return return_dict
