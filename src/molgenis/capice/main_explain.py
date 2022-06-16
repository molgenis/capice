import os
import pandas as pd
import xgboost as xgb

from molgenis.capice.main_capice import Main
from molgenis.capice.core.logger import Logger
from molgenis.capice.core.capice_manager import CapiceManager


class CapiceExplain(Main):
    def __init__(self, model, output_path):
        super().__init__(input_path=None, output_path=output_path)
        self.model = model
        self.output = output_path
        self.log = Logger().logger

    def run(self):
        importances = self._extract_features_importances(self.model)
        importances = self._convert_importances_to_dataframe(importances)
        self._order_importances(importances)
        self._export(importances, self.output)

    def _extract_features_importances(self, model: xgb.XGBClassifier):
        self.log.info('Extracting features from model.')
        feature_importances = model.get_booster().get_score(importance_type='gain')
        self.log.debug('Extracted %d features from model.', len(feature_importances.keys()))
        return feature_importances

    def _convert_importances_to_dataframe(self, importances: dict):
        self.log.info('Converting importances to dataframe.')
        feature_importances = pd.DataFrame(data=[importances.keys(), importances.values()], index=['feature', 'gain']).T
        self.log.debug('Converted %d features into the dataframe', feature_importances.shape[0])
        return feature_importances

    def _order_importances(self, importances: pd.DataFrame):
        self.log.info('Ordering feature importances.')
        importances.sort_values(by='gain', ascending=False, inplace=True)

    def _export(self, dataset, output):
        output_path = os.path.join(output, CapiceManager().output_filename)
        dataset.to_csv(output_path, compression='gzip', index=False)
        self.log.info('Successfully exported explain to: %s', output_path)
