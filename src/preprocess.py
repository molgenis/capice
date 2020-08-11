from src.logger import Logger
import pandas as pd
import numpy as np


class PreProcess:
    def __init__(self):
        self.log = Logger().get_logger()
        self.cadd_vars = []
        self.impute_values = {}
        self.data = pd.DataFrame()
        pass

    def preprocess(self, data, impute_values, cadd_vars, train=False):
        """
        Preprocessing the data to be able to get used in CAPICE.
        :param data: pd.DataFrame
        :param impute_values: dict
        :param cadd_vars: list
        :param train: bool
        :return: pd.DataFrame
        """
        self.impute_values = impute_values
        self.cadd_vars = cadd_vars
        self._process_impute(data)

        # First get cadd vars
        # Then impute [done]
        # then preprocess
        pass

    def get_cadd_vars(self):
        """
        Function to return the ca
        :return:
        """
        return self.cadd_vars

    def _process_impute(self, data):
        self.log.info('Starting imputing, removing rows with no data at all.')
        before_drop = data.shape[0]
        data.dropna(subset=self.cadd_vars, how='all', inplace=True)
        after_drop = data.shape[0]
        self.log.info(
            'Removed {} rows with no data.'.format(
                before_drop - after_drop)
        )
        data['dbscSNV-rf_score_copy'] = data['dbscSNV-rf_score']
        data['dbscSNV-rf_score'] = data['dbscSNV-rf_score_copy'].apply(
            lambda x: self._dbsc_snv_rf_score_nan_func(x))
        data.drop(columns=['dbscSNV-rf_score_copy'], inplace=True)
        data.dropna(how='all', inplace=True)
        self.log.info('NaN\'s have been dropped, final data shape: {}'.format(
            data.shape
        ))
        self._examine_nan(data)
        data = self._impute(data)
        self.log.info('NaN\'s replaced, rechecking:')
        self._examine_nan(data)
        self.data = data

    def _impute(self, data):
        for col in data.columns:
            if data[col].isna().any() and col in self.impute_values.keys():
                self.log.info(
                    'Encountered NaN in {}, replacing with {}'.format(
                        col, self.impute_values[col]
                    )
                )
                data[col].fillna(self.impute_values[col], inplace=True)
        return data

    def _examine_nan(self, data):
        n_samples = data.shape[0]
        for col in data.columns:
            n_nan = data[col].isnull().sum()
            if n_nan > 0:
                p_nan = round(n_nan / n_samples * 100, 2)
                self.log.info('Column {} has a NaN percentage of: {}'.format(
                    col, p_nan
                ))

    @staticmethod
    def _dbsc_snv_rf_score_nan_func(x):
        if pd.isnull(x) or x == '.' or x == 'NA':
            return np.NaN
        else:
            return float(x)
