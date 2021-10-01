import os
import pandas as pd
from src.main.python.core.global_manager import CapiceManager
from src.main.python.core.logger import Logger
from src.main.python.resources.errors.errors import InitializationError
from src.main.python.resources.utilities.utilities import get_project_root_dir
from src.main.python.resources.utilities.dynamic_loader import DynamicLoader


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
        self.overwrite = self.manager.overwrite_model
        self.vep_version = self.manager.vep_version
        self.grch_build = self.manager.grch_build
        self.train = is_train
        self.module = None

    def _load_preprocessors(self):
        """
        Function to dynamically load in the preprocessors modules,
        but must have the following properties:
            name,
            _get_model_loc
        within the models directory. Will set self.module according to the
        train flag, overwrite, VEP version and GRCh build.
        """
        self.log.info('Identifying preprocessing files.')
        directory = os.path.join(get_project_root_dir(),
                                 'src',
                                 'main',
                                 'python',
                                 'resources',
                                 'models')
        dynamic_loader = DynamicLoader(
            required_attributes=['name', '_get_model_loc'],
            path=directory
        )
        self.module = dynamic_loader.load_impute_preprocess_modules(
            vep_version=self.vep_version,
            grch_build=self.grch_build,
            overwrite=self.overwrite,
            train=self.train
        )

    def preprocess(self, datafile: pd.DataFrame):
        """
        Callable function for external modules to start call the preprocessor
        of the correctly chosen module.
        :param datafile: unprocessed pandas DataFrame
        :return: processed pandas Dataframe
        """
        self._load_preprocessors()
        processed_data = self.module.preprocess(
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
        predicted_data = self.module.predict(data=datafile)
        return predicted_data

    def get_model_features(self):
        if self.module is None:
            error_message = "Preprocessor has to be initialized before " \
                            "model features can be requested."
            self.log.critical(error_message)
            raise InitializationError(error_message)
        return self.module.model_features
