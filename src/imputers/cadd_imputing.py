from src.data_files.cadd14_grch37 import Cadd14Grch37
from src.logger import Logger
import pandas as pd


class CaddImputing:
    """
    What I need for this class is the CADD version and GRCh build
    """
    def __init__(self, cadd_version, grch_build):
        self.cadd_version = cadd_version
        self.grch_build = grch_build
        self.log = Logger().get_logger()
        self.log.info('Starting imputing.')
        self.modules = [Cadd14Grch37()]
        self.module = None
        self._is_correct_datafile_present()
        self.columns = []
        self.impute_values = {}

    def _is_correct_datafile_present(self):
        for module in self.modules:
            if module.version_check(self.cadd_version) and module.build_check(self.grch_build):
                self.log.info('Impute data file successfully found: {}'.format(module.get_name()))
                self.module = module

        # Checking if self.data_file is assigned
        if self.module is None:
            error_message = 'No imputing data file found for CADD version: {} and genome build: {}'.format(
                self.cadd_version,
                self.grch_build
            )
            self.log.critical(error_message)
            raise FileNotFoundError(error_message)

    def _load_values(self):
        self.columns = self.module.get_cadd_features()
        self.impute_values = self.module.get_impute_values()

    def impute(self, datafile: pd.DataFrame):
        """
        Function to call the CaddImputing to start imputing
        :return: pandas DataFrame
        """
        self._load_values()
        datafile = self._set_dataset(datafile)
        datafile = self._check_chrom_pos(datafile)
        self._get_nan_ratio_per_column(
            dataset=datafile
        )
        self._get_full_nan_row(
            dataset=datafile
        )
        datafile.dropna(how='all', subset=self.columns)
        datafile.fillna(self.impute_values, inplace=True)
        self.log.info('Imputing successfully performed.')
        return datafile

    def _set_dataset(self, dataset: pd.DataFrame):
        return dataset[self.columns]

    def _check_chrom_pos(self, dataset: pd.DataFrame):
        if dataset['#Chrom'].isnull().values.any():
            n_delete = dataset['#Chrom'].isnull().values.sum()
            self.log.warning('Detected NaN in the Chromosome column! Deleting {} row(s).'.format(n_delete))
            dataset = dataset[~dataset['#Chrom'].isnull()]
        if dataset['Pos'].isnull().values.any():
            n_delete = dataset['Pos'].isnull().values.sum()
            self.log.warning('Detected NaN is the Position column! Deleting {} row(s).'.format(n_delete))
            dataset = dataset[~dataset['#Chrom'].isnull()]
        return dataset

    def _get_nan_ratio_per_column(self, dataset: pd.DataFrame):
        n_samples = dataset.shape[0]
        for column in dataset.columns:
            n_nan = dataset[column].isnull().sum()
            if n_nan > 0:
                p_nan = (n_nan / n_samples) * 100
                self.log.info('NaN detected in column {}, percentage: {}%.'.format(
                    column,
                    p_nan
                ))

    def _get_full_nan_row(self, dataset: pd.DataFrame):
        n_samples = dataset.shape[0]
        dataset.index = range(1, n_samples + 1)
        dataset['CAPICE_drop_out'] = dataset.isnull().values.all(axis=1)
        samples_dropped_out = dataset[dataset['CAPICE_drop_out']]
        if samples_dropped_out.shape[0] > 0:
            self.log.warning('The following samples are filtered out due to missing values: (indexing is python based, '
                             'so the index starts at 0). \n {}'.format(samples_dropped_out['#Chrom', 'Pos', 'Ref', 'Alt'])
                             )
        else:
            self.log.info('No samples are filtered out due to too many NaN values.')
