import os

import pandas as pd
import xgboost as xgb

from molgenis.capice.main_capice import Main
from molgenis.capice.core.logger import Logger
from molgenis.capice.core.capice_manager import CapiceManager


class CapiceExplain(Main):
    def __init__(self, model, output_path, output_given):
        super().__init__(input_path=None, output_path=output_path, output_given=output_given)
        self.model = model
        self.output = output_path
        self.log = Logger().logger

    def run(self):
        gain_importances = self._extract_features_importances_gain(self.model)
        total_gain_importances = self._extract_features_importances_total_gain(self.model)
        weight_importances = self._extract_features_importances_weight(self.model)
        cover_importances = self._extract_features_importances_cover(self.model)
        total_cover_importances = self._extract_features_importances_total_cover(self.model)
        importances = self._convert_importances_to_dataframe(gain_importances,
                                                             total_gain_importances,
                                                             weight_importances,
                                                             cover_importances,
                                                             total_cover_importances)
        self._order_importances(importances)
        self._export(importances, self.output)

    def _extract_features_importances_gain(self, model: xgb.XGBClassifier):
        self.log.info('Extracting gain from model.')
        feature_importances = model.get_booster().get_score(importance_type='gain')
        self.log.debug('Extracted %d gain features from model.', len(feature_importances.keys()))
        return feature_importances

    def _extract_features_importances_total_gain(self, model: xgb.XGBClassifier):
        self.log.info('Extracting total gain from model.')
        feature_importances = model.get_booster().get_score(importance_type='total_gain')
        self.log.debug('Extracted %d total_gain features from model.',
                       len(feature_importances.keys()))
        return feature_importances

    def _extract_features_importances_weight(self, model: xgb.XGBClassifier):
        self.log.info('Extracting weight from model.')
        feature_importances = model.get_booster().get_score(importance_type='weight')
        self.log.debug('Extracted %d weight features from model.',
                       len(feature_importances.keys()))
        return feature_importances

    def _extract_features_importances_cover(self, model: xgb.XGBClassifier):
        self.log.info('Extracting cover from model.')
        feature_importances = model.get_booster().get_score(importance_type='cover')
        self.log.debug('Extracted %d cover features from model.',
                       len(feature_importances.keys()))
        return feature_importances

    def _extract_features_importances_total_cover(self, model: xgb.XGBClassifier):
        self.log.info('Extracting total cover from model.')
        feature_importances = model.get_booster().get_score(importance_type='total_cover')
        self.log.debug('Extracted %d total_cover features from model.',
                       len(feature_importances.keys()))
        return feature_importances

    def _convert_importances_to_dataframe(self, gain: dict, total_gain: dict, weight: dict,
                                          cover: dict, total_cover: dict):
        self.log.info('Converting importances to dataframe.')
        feature_importances = pd.DataFrame(data=[gain.keys(), gain.values()],
                                           index=['feature', 'gain']).T
        feature_importances['total_gain'] = feature_importances['feature'].map(total_gain)
        feature_importances['weight'] = feature_importances['feature'].map(weight)
        feature_importances['cover'] = feature_importances['feature'].map(cover)
        feature_importances['total_cover'] = feature_importances['feature'].map(total_cover)
        self.log.debug('Converted %d features into the dataframe', feature_importances.shape[0])
        self.log.debug('Converted all %d importance types into the dataframe',
                       feature_importances.shape[1])
        return feature_importances

    def _order_importances(self, importances: pd.DataFrame):
        self.log.info('Ordering feature importances.')
        importances.sort_values(by='gain', ascending=False, inplace=True)

    def _export(self, dataset, output):
        output_path = os.path.join(output, CapiceManager().output_filename)
        dataset.to_csv(output_path, compression='gzip', index=False, sep='\t')
        if not self.output_given:
            print(f'Successfully exported explain to: {output_path}')
