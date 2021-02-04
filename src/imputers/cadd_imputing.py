from src.logger import Logger
import inspect
from src.utilities.utilities import get_project_root_dir, load_modules, importer
from src.global_manager import CapiceManager
import pandas as pd
import os


class CaddImputing:
    """
    What I need for this class is the CADD version and GRCh build
    """
    def __init__(self):
        self.manager = CapiceManager()
        self.cadd_version = self.manager.get_cadd_version()
        self.grch_build = self.manager.get_grch_build()
        self.log = Logger().get_logger()
        self.log.info('Imputer started.')
        self.overrule = self.manager.get_overwrite_impute()
        self.modules = []
        self.module = None
        self._load_modules()
        self._is_correct_datafile_present()
        self.columns = []
        self.impute_values = {}

    def _load_modules(self):
        self.log.info('Identifying imputing files.')
        directory = os.path.join(get_project_root_dir(), 'src', 'data_files', 'imputing')
        usable_modules = load_modules(directory)
        if len(usable_modules) < 1:
            self._raise_no_module_found_error()
        loaded_modules = importer(usable_modules=usable_modules, path=directory)
        for module in loaded_modules:
            if "get_name" in dir(module) and "_cadd_features" in dir(module) and "_impute_values" in dir(module):
                self.modules.append(module)
        if len(self.modules) < 1:
            self._raise_no_module_found_error()
        self.log.info('Identified {} files available for usage in imputing.'.format(len(self.modules)))

    def _raise_no_module_found_error(self):
        error_message = 'No usable python files are found within the imputing directory!'
        self.log.critical(error_message)
        raise FileNotFoundError(error_message)

    def _is_correct_datafile_present(self):
        for module in self.modules:
            if self.overrule:
                if module.get_name() == self.overrule:
                    self.log.info('Overrule successful for: {} , located at: {}'.format(
                        self.overrule, inspect.getfile(module.__class__)))
                    self.module = module
                    break
            else:
                if module.version_check(self.cadd_version) and module.build_check(self.grch_build):
                    self.log.info('Impute data file successfully found: {} , located at: {}'.format(
                        module.get_name(), inspect.getfile(module.__class__)))
                    self.module = module
                    break

        # Checking if self.data_file is assigned
        if self.module is None:
            if self.overrule:
                error_message = 'No imputing data file found for overrule: {}'.format(
                    self.overrule
                )
            else:
                error_message = 'No imputing data file found for CADD version: {} and genome build: {}'.format(
                    self.cadd_version,
                    self.grch_build
                )
            self.log.critical(error_message)
            raise FileNotFoundError(error_message)

    def _load_values(self):
        self.columns = self.module.get_cadd_features()
        self.manager.set_cadd_features(self.columns)
        self.impute_values = self.module.get_impute_values()

    def impute(self, datafile: pd.DataFrame):
        """
        Function to call the CaddImputing to start imputing
        :return: pandas DataFrame
        """
        self._load_values()
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
                p_nan = round((n_nan / n_samples) * 100, ndigits=2)
                self.log.debug('NaN detected in column {}, percentage: {}%.'.format(
                    column,
                    p_nan
                ))

    def _get_full_nan_row(self, dataset: pd.DataFrame):
        n_samples = dataset.shape[0]
        dataset.index = range(1, n_samples + 1)
        dataset['CAPICE_drop_out'] = dataset[self.columns].isnull().values.all(axis=1)
        samples_dropped_out = dataset[dataset['CAPICE_drop_out']]
        if samples_dropped_out.shape[0] > 0:
            self.log.warning('The following samples are filtered out due to missing values: (indexing is python based, '
                             'so the index starts at 0). \n {}'.format(
                                samples_dropped_out[['#Chrom', 'Pos', 'Ref', 'Alt', 'FeatureID']])
                             )
        else:
            self.log.info('No samples are filtered out due to too many NaN values.')
