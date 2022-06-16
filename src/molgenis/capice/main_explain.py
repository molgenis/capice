import os
import pandas as pd
import xgboost as xgb

from molgenis.capice.main_capice import Main
from molgenis.capice.core.capice_manager import CapiceManager


class CapiceExplain(Main):
    def __init__(self, model, output_path):
        super().__init__(input_path=None, output_path=output_path)
        self.model = model
        self.output = output_path

    def run(self):
        importances = self._extract_features_importances(self.model)
        importances = self._convert_importances_to_dataframe(importances)
        self._order_importances(importances)
        self._export(importances, self.output)

    @staticmethod
    def _extract_features_importances(model: xgb.XGBClassifier):
        feature_importances = model.get_booster().get_score(importance_type='gain')
        return feature_importances

    @staticmethod
    def _convert_importances_to_dataframe(importances: dict):
        feature_importances = pd.DataFrame(data=[importances.keys(), importances.values()], index=['feature', 'gain']).T
        return feature_importances

    @staticmethod
    def _order_importances(importances: pd.DataFrame):
        importances.sort_values(by='gain', ascending=False, inplace=True)

    @staticmethod
    def _export(dataset, output):
        dataset.to_csv(os.path.join(output, CapiceManager().output_filename), compression='gzip', index=False)
