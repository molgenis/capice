"""
File that contains all information specific to the originally published CAPICE
model using XGBoost 0.72.1.
"""

from src.main.python.resources.models.model_abstract import TemplateSetup
from src.main.python.resources.utilities.utilities import get_project_root_dir
import os
from xgboost import DMatrix


class ModelSetupXGBoost0721(TemplateSetup):
    """
    Model setup for XGBoost version 0.72.1, CADD 1.4 and genome build 37.
    """
    def __init__(self):
        super().__init__(
            name="CAPICE using XGBoost 0.72.1, CADD 1.4 and genome build 37.",
            usable=False,
            vep_version=104.0,
            grch_build=37
        )

    @staticmethod
    def _get_model_loc():
        model_loc = os.path.join(
            get_project_root_dir(),
            'CAPICE_model',
            'GRCh37',
            'xgb_booster.pickle.dat'
        )
        return model_loc

    def _load_model_features(self):
        self.model_features = self.model.feature_names

    def _predict(self, predict_data):
        return self.model.predict(predict_data)

    def _create_input_matrix(self, dataset):
        return DMatrix(dataset[self.model_features])
