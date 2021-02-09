from src.utilities.utilities import get_project_root_dir, load_modules, importer
import inspect
from src.logger import Logger
from src.global_manager import CapiceManager
import pandas as pd
import os


class PreProcessor:
    """
    Class to dynamically load in all model files for preprocessing and choosing the correct preprocessing file
    according to the given command line arguments or parsed CADD file header. (or the --overwrite_model_file argument)
    """
    def __init__(self, is_train: bool = False):
        self.manager = CapiceManager()
        self.log = Logger().get_logger()
        self.log.info('Preprocessor started.')
        self.overrule = self.manager.get_overwrite_model()
        self.cadd_version = self.manager.get_cadd_version()
        self.grch_version = self.manager.get_grch_build()
        self.train = is_train
        self.preprocessors = []
        self.preprocessor = None
        self._prepare_preprocessor()

    def _prepare_preprocessor(self):
        """
        Function to see if the training protocol should be used or the preprocessors should be loaded in.
        """
        if self.train:
            from src.models.training_preprocessor import TrainPreprocessor
            self.preprocessor = TrainPreprocessor()
        else:
            self._load_preprocessors()
            self._load_correct_preprocessor()

    def _load_preprocessors(self):
        """
        Function to dynamically load in the preprocessors modules, but must have the following functions: get_name(),
        get_supported_cadd_version() and get_supported_genomebuild_version().
        """
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
        """
        Specialized function to be used into _load_preprocessors() and _load_correct_preprocessor() to be raised when
        no preprocessing files can be found.
        """
        error_message = 'No usable python files are found within the imputing directory!'
        self.log.critical(error_message)
        raise FileNotFoundError(error_message)

    def _load_correct_preprocessor(self):
        """
        Function to check the dynamically loaded preprocessors to match either the overrule argument or
        the cadd version and genome build.
        """
        for preprocessor in self.preprocessors:
            if self.overrule:
                if preprocessor.get_name() == self.overrule:
                    self.log.info('Overrule successful for: {} , located at: {}'.format(
                        self.overrule, inspect.getfile(preprocessor.__class__)))
                    self.preprocessor = preprocessor
                    break
            else:
                module_cadd = preprocessor.get_supported_cadd_version()
                module_grch = preprocessor.get_supported_genomebuild_version()
                if module_cadd == self.cadd_version and module_grch == self.grch_version:
                    self.log.info('Preprocessing and model file successfully found: {} , Located at: {}'.format(
                        preprocessor.get_name(), inspect.getfile(preprocessor.__class__)))
                    self.preprocessor = preprocessor
                    break

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
        """
        Callable function for external modules to start call the preprocessor of the correctly chosen module.
        :param datafile: unprocessed pandas DataFrame
        :return: processed pandas Dataframe
        """
        processed_data = self.preprocessor.preprocess(dataset=datafile, is_train=self.train)
        return processed_data

    def predict(self, datafile: pd.DataFrame):
        """
        Callable function for external modules to start the call to the predict of the correctly chosen module.
        :param datafile: preprocessed pandas DataFrame
        :return: predicted pandas DataFrame
        """
        predicted_data = self.preprocessor.predict(data=datafile)
        return predicted_data
