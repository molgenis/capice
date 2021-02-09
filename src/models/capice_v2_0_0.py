"""
File to contain all specific information for the updated XGBoost 1.1.1 model, created in the same way as the
original model was.
"""

from src.models.model_abstract import TemplateSetup
from src.utilities.utilities import get_project_root_dir
import os


class XGBoost111(TemplateSetup):
    @staticmethod
    def get_name():
        return "CAPICE using XGBoost 1.1.1, CADD 1.4 and genome build 37."

    @staticmethod
    def is_usable():
        return True

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
