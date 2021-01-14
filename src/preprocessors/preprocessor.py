from src.utilities.utilities import get_project_root_dir, load_modules, importer
from importlib import import_module
from src.logger import Logger
from src.global_manager import CapiceManager
import pandas as pd
import os


class PreProcessor:
    def __init__(self, is_train: bool = False):
        self.manager = CapiceManager()
        self.log = Logger().get_logger()
        self.log.info('Preprocessor started.')
        self.overrule = self.manager.get_overwrite_model()
        self.cadd_version = self.manager.get_cadd_version()
        self.grch_version = self.manager.get_grch_build()
        self.train = is_train
        self.preprocessors = []
        self._load_preprocessors()
        self.preprocessor = None

    def _load_preprocessors(self):
        self.log.info('Identifying preprocessing files.')
        directory = os.path.join(get_project_root_dir(), 'src', 'models')
        usable_modules = load_modules(directory)
        if len(usable_modules) < 1:
            self._raise_no_module_found_error()
        imported_modules = importer(usable_modules=usable_modules, path=directory)
        for module in imported_modules:
            if "get_name" in dir(module) and "get_supported_cadd_version" in dir(
                    module) and "get_supported_genomebuild_version" in dir(module):
                self.preprocessors.append(module)
        if len(self.preprocessors) < 1:
            self._raise_no_module_found_error()
        self.log.info('Succesfully loaded {} preprocessors.'.format(len(self.preprocessors)))

    def _raise_no_module_found_error(self):
        error_message = 'No usable python files are found within the imputing directory!'
        self.log.critical(error_message)
        raise FileNotFoundError(error_message)

    def _load_correct_preprocessor(self):
        for preprocessor in self.preprocessors:
            if self.overrule:
                if preprocessor.get_name() == self.overrule:
                    self.log.info('Overrule successful for: {}'.format(self.overrule))
                    self.preprocessor = preprocessor
            else:
                module_cadd = preprocessor.get_supported_cadd_version()
                module_grch = preprocessor.get_supported_genomebuild_version()
                if module_cadd == self.cadd_version and module_grch == self.grch_version:
                    self.log.info('Preprocessing and model file successfully found: {}'.format(preprocessor))
        if self.preprocessor is None:
            if self.overrule:
                error_message = 'No model data file found for overrule: {}'.format(
                    self.overrule
                )
            else:
                error_message = 'No model data file found for CADD version: {} and genome build: {}'.format(
                     self.cadd_version,
                     self.grch_version
                )
            self.log.critical(error_message)
            raise FileNotFoundError(error_message)

    def preprocess(self, datafile: pd.DataFrame):
        self._load_correct_preprocessor()
        processed_data = self.preprocessor.preprocess(dataset=datafile, is_train=self.train)
        return processed_data

    def predict(self, datafile: pd.DataFrame):
        predicted_data = self.preprocessor.predict(data=datafile)
        return predicted_data
