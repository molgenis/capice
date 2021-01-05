from src.utilities.utilities import get_project_root_dir, load_modules
from importlib import import_module
from src.logger import Logger
import pandas as pd
import sys
import os


class PreProcessor:
    def __init__(self, cadd_features: list, is_train: bool = False):
        self.log = Logger().get_logger()
        self.log.info('Preprocessor started.')
        self.cadd_features = cadd_features
        self.train = is_train
        self.preprocessors = []
        self._load_preprocessors()

    def _load_preprocessors(self):
        self.log.info('Identifying preprocessing files.')
        directory = os.path.join(get_project_root_dir(), 'src', 'models')
        sys.path.append(directory)
        usable_modules = load_modules(directory)
        if len(usable_modules) < 1:
            self._raise_no_module_found_error()
        for module in usable_modules:
            mod = import_module(module)
            if "get_preprocessing_name" in dir(mod) and "get_supported_cadd_version" in dir(
                    mod) and "get_supported_genomebuild_version" in dir(mod):
                self.preprocessors.append(mod)
        if len(self.preprocessors) < 1:
            self._raise_no_module_found_error()
        self.log.info('Succesfully loaded {} preprocessors.'.format(len(self.preprocessors)))

    def _raise_no_module_found_error(self):
        error_message = 'No usable python files are found within the imputing directory!'
        self.log.critical(error_message)
        raise FileNotFoundError(error_message)

    def preprocess(self, datafile: pd.DataFrame):
        pass
