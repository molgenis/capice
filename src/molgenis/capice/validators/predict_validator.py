import pandas as pd
import xgboost as xgb

from molgenis.capice.core.logger import Logger


class PredictValidator:
    def __init__(self):
        self.log = Logger().logger

    def validate_data_predict_ready(self, dataset: pd.DataFrame, model: xgb.XGBClassifier) ->\
            None:
        """
        Validates if dataset is predict ready according to the feature names in model

        Args:
            dataset:
                The dataset that is supposed to be predict ready.
            model:
                The custom CAPICE xgboost.XGBClassifier.
        Raises:
            KeyError:
                Raised when a required predict feature is missing from dataset.
        """
        missing = []
        for feature in model.get_booster().feature_names:  # type: ignore
            if feature not in dataset.columns:
                missing.append(feature)
        if len(missing) > 0:
            error_message = 'Missing required predict column(s): %s'
            self.log.critical(error_message, ', '.join(missing))
            raise KeyError(error_message, ', '.join(missing))
