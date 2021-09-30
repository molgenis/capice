import inspect
import os

import pandas as pd

from src.main.python.core.global_manager import CapiceManager
from src.main.python.core.logger import Logger
from src.main.python.resources.errors.errors import InitializationError
from src.main.python.resources.utilities.utilities import \
    get_project_root_dir, load_modules, importer


class PreProcessor:
    """
    Class to dynamically load in all model files for preprocessing and choosing
    the correct preprocessing file according to the given config arguments or
    parsed VEP file header. (or the --overwrite_model_file argument)
    """
    def __init__(self, is_train: bool = False):
        self.log = Logger().logger
        self.manager = CapiceManager()
        self.log.info('Preprocessor started.')
        self.overrule = self.manager.overwrite_model
        self.vep_version = self.manager.vep_version
        self.grch_build = self.manager.grch_build
        self.train = is_train
        self.preprocessors = []
        self.preprocessor = None
        self._prepare_preprocessor()

    def _prepare_preprocessor(self):
        """
        Function to see if the training protocol should be used or the
        preprocessors should be loaded in.
        """
        if self.train:
            from src.main.python.resources.models.training_preprocessor import \
                TrainPreprocessor
            self.preprocessor = TrainPreprocessor()
        else:
            self._load_preprocessors()
            self._load_correct_preprocessor()
        self._check_preprocessor_is_applied()

    def _load_preprocessors(self):
        """
        Function to dynamically load in the preprocessors modules,
        but must have the following properties:
            name,
            supported_vep_version and
            supported_genomebuild_version.
        """
        self.log.info('Identifying preprocessing files.')
        directory = os.path.join(get_project_root_dir(),
                                 'src',
                                 'main',
                                 'python',
                                 'resources',
                                 'models')
        usable_modules = load_modules(directory)
        if len(usable_modules) < 1:
            self._raise_no_module_found_error()
        imported_modules = importer(
            usable_modules=usable_modules,
            path=directory
        )
        for module in imported_modules:
            if "name" in dir(module) and "supported_vep_version" in dir(
                    module) and "supported_grch_build" in dir(module):
                self.preprocessors.append(module)
        if len(self.preprocessors) < 1:
            self._raise_no_module_found_error()
        self.log.info(
            'Successfully loaded %s preprocessors.', len(self.preprocessors)
        )

    def _raise_no_module_found_error(self):
        """
        Specialized function to be used into
            _load_preprocessors() and
            _load_correct_preprocessor()
        to be raised when no preprocessing files can be found.
        """
        error_message = 'No usable python files are ' \
                        'found within the model directory!'
        self.log.critical(error_message)
        raise FileNotFoundError(error_message)

    def _raise_module_not_found_error(self, module_name):
        """
        Specialized function to be used into
            _load_preprocessors() and
            _load_correct_preprocessor()
        to be raised when specific preprocessing file can not be found.
        """
        error_message = f'The module "{module_name}" could not be found ' \
                        f'within the model directory!'
        self.log.critical(error_message)
        raise FileNotFoundError(error_message)

    def _load_correct_preprocessor(self):
        """
        Function to check the dynamically loaded preprocessors to match either
        the overrule argument or the vep version and genome build.
        """
        if self.overrule:
            for preprocessor in self.preprocessors:
                if preprocessor.name == self.overrule:
                    self.log.info(
                        'Overrule successful for: %s , '
                        'located at: %s', self.overrule,
                        inspect.getfile(preprocessor.__class__)
                    )
                    self.preprocessor = preprocessor
                    return
            # If no match found, triggers error.
            self._raise_module_not_found_error(self.overrule)
        else:
            for preprocessor in self.preprocessors:
                module_vep = preprocessor.supported_vep_version
                module_grch = preprocessor.supported_grch_build
                if module_vep == self.vep_version and \
                        module_grch == self.grch_build:
                    self.log.info(
                        'Preprocessing and model file successfully found: %s, '
                        'Located at: %s',
                        preprocessor.name,
                        inspect.getfile(preprocessor.__class__)
                    )
                    self.preprocessor = preprocessor
                    return
            # If no match found, triggers error.
            self._raise_no_module_found_error()

    def _check_preprocessor_is_applied(self):
        if self.preprocessor is None:
            if self.overrule:
                error_message = 'No model data file found for overrule: ' \
                                '{}'.format(self.overrule)
            else:
                error_message = f'No model data file found for VEP version: ' \
                                f'{self.vep_version} and genome build: ' \
                                f'{self.grch_build}'
            self.log.critical(error_message)
            raise FileNotFoundError(error_message)

    def preprocess(self, datafile: pd.DataFrame):
        """
        Callable function for external modules to start call the preprocessor
        of the correctly chosen module.
        :param datafile: unprocessed pandas DataFrame
        :return: processed pandas Dataframe
        """
        processed_data = self.preprocessor.preprocess(
            dataset=datafile,
            is_train=self.train
        )
        return processed_data

    def predict(self, datafile: pd.DataFrame):
        """
        Callable function for external modules to start the call to the
        predict of the correctly chosen module.
        :param datafile: preprocessed pandas DataFrame
        :return: predicted pandas DataFrame
        """
        predicted_data = self.preprocessor.predict(data=datafile)
        return predicted_data

    def get_model_features(self):
        if self.preprocessor is None:
            error_message = "Preprocessor has to be initialized before " \
                            "model features can be requested."
            self.log.critical(error_message)
            raise InitializationError(error_message)
        return self.preprocessor.model_features
