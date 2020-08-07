from src.models.abstract_model import ModelSetup
import xgboost as xgb
import pickle


class ModelSetupXGBoost0721(ModelSetup):
    """
    Model setup for XGBoost version 0.72.1, CADD 1.4 and genome build 37.
    """
    def __init__(self):
        self.model = None
        self.model_feats = []

    def get_name(self):
        return "XGBoost version 0.72.1, CADD 1.4 and Genome Build 37"

    @staticmethod
    def get_xgb_version():
        if int(xgb.__version__.split(".")[0]) < 1:
            return True

    @staticmethod
    def get_supported_cadd_version():
        return 1.4

    @staticmethod
    def get_supported_genomebuild_version():
        return 37

    def predict(self, data):
        self._load_model()
        input_matrix = xgb.DMatrix(data[self.model_feats])
        data['probabilities'] = self.model.predict(input_matrix)
        return data

    def _load_model(self):
        self.model = pickle.load(
            open(
                '../../CAPICE_model/xgb_booster.pickle.dat', 'rb'
            )
        )
        self.model_feats = self.model.feature_names
