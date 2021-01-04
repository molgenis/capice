from src.models.model_abstract import ModelSetup
from src.utilities.utilities import get_project_root_dir
import os


class ModelSetupXGBoost111(ModelSetup):
    """
    Model setup for XGBoost version 1.1.1, CADD 1.4 and genome build 37.
    """
    @staticmethod
    def get_name():
        return "CAPICE using XGBoost 0.72.1, CADD 1.4 and genome build 37."

    @staticmethod
    def get_supported_cadd_version():
        return 1.4

    @staticmethod
    def get_supported_genomebuild_version():
        return 37

    @staticmethod
    def _get_model_loc():
        model_loc = os.path.join(get_project_root_dir(), 'CAPICE_model', 'xgb_booster37.pickle.dat')
        return model_loc
