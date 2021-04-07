"""
File to contain all specific information for the updated XGBoost 1.1.1 model, created in the same way as the
original model was.
"""

from src.main.python.resources.models.model_abstract import TemplateSetup
from src.main.python.resources.utilities.utilities import get_project_root_dir
import os


class XGBoost111(TemplateSetup):
    def __init__(self):
        super().__init__(
            name="CAPICE using XGBoost 1.1.1, CADD 1.4 and genome build 37.",
            usable=True,
            cadd_version=1.4,
            grch_build=37
        )

    @staticmethod
    def _get_model_loc():
        model_loc = os.path.join(get_project_root_dir(), 'CAPICE_model', 'xgb_booster37.pickle.dat')
        return model_loc
