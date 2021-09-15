"""
File that contains all information for a POC CAPICE model using XGBoost 1.4.2.
"""

from src.main.python.resources.models.model_abstract import TemplateSetup
from src.main.python.resources.utilities.utilities import get_project_root_dir
import os
from xgboost import DMatrix


class ModelSetupXGBoost142POC(TemplateSetup):
    """
    Model setup for XGBoost version 1.4.2, VEP104.2 and genome build 37.
    """
    def __init__(self):
        super().__init__(
            name="CAPICE POC using XGBoost 1.4.2, VEP104 and genome build 37.",
            usable=True,
            vep_version=104.0,
            grch_build=37
        )

    @staticmethod
    def _get_model_loc():
        model_loc = os.path.join(
            get_project_root_dir(),
            'CAPICE_model',
            'GRCh37',
            'POC',
            'xgb_booster_poc.pickle.dat'
        )
        return model_loc
