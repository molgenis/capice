from src.models.abstract_model import ModelSetup
import xgboost as xgb
import pickle


class ModelSetupXGBoost111(ModelSetup):
    """
    Model setup for XGBoost version 1.1.1, CADD 1.4 and genome build 37.
    """
    def __init__(self):
        self.model = None
        self.model_feats = []

    def get_name(self):
        return "XGBoost version 1.1.1, CADD 1.4 and Genome Build 37"

    @staticmethod
    def get_xgb_version():
        """
        Known that XGBoost 1.1.1 is supported, has to be investigated
        if future and past versions work with this setup.
        """
        if xgb.__version__ == '1.1.1':
            return True

    @staticmethod
    def get_supported_cadd_version():
        return 1.4

    @staticmethod
    def get_supported_genomebuild_version():
        return 37

    def predict(self, data):
        self._load_model()
        data['probabilites'] = self.model.predict_proba(
            data[self.model_feats]
        )[:, 1]
        return data

    def _load_model(self):
        self.model = pickle.load(
            open(
                '../../CAPICE_model/xgb_booster37.pickle.dat', 'rb'
            )
        )
        self.model_feats = self.model._Booster.feature_names
