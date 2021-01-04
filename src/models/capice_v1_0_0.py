from src.models.model_abstract import ModelSetup
from src.utilities.utilities import get_project_root_dir
import os
from xgboost import DMatrix


class ModelSetupXGBoost0721(ModelSetup):
    """
    Model setup for XGBoost version 0.72.1, CADD 1.4 and genome build 37.
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
        model_loc = os.path.join(get_project_root_dir(), 'CAPICE_Model', 'GRCh37', 'xgb_booster.pickle.dat')
        return model_loc

    def _load_model_features(self):
        return self.model.feature_names

    def _predict(self, predict_data):
        return self.model.predict(predict_data)

    def _create_input_matrix(self, dataset):
        return DMatrix(dataset[self.model_features])
