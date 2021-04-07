from src.main.python.core.logger import Logger
import inspect
from src.main.python.resources.utilities.utilities import get_project_root_dir, load_modules, importer
from src.main.python.core.global_manager import CapiceManager
import pandas as pd
import os


class CaddImputing:
    """
    Class to dynamically load in all imputing files and identify the file suitable for the run's use case.
    """

    def __init__(self):
        self.manager = CapiceManager()
        self.cadd_version = self.manager.cadd_version
        self.grch_build = self.manager.grch_build
        self.log = Logger().logger
        self.log.info('Imputer started.')
        self.overrule = self.manager.overwrite_impute
        self.modules = []
        self.module = None
        self._load_modules()
        self._is_correct_datafile_present()
        self.columns = []
        self.impute_values = {}

    def _load_modules(self):
        """
        Method to dynamically load in all python files containing a class that contains the functions get_name(),
        _cadd_features() and _impute_values(). If at the end of this function, the list of impute files is empty,
        will throw the module not found error.
        """
        self.log.info('Identifying imputing files.')
        directory = os.path.join(get_project_root_dir(),
                                 'src',
                                 'main',
                                 'python',
                                 'resources',
                                 'data_files',
                                 'imputing')
        usable_modules = load_modules(directory)
        if len(usable_modules) < 1:
            self._raise_no_module_found_error()
        loaded_modules = importer(usable_modules=usable_modules, path=directory)
        for module in loaded_modules:
            if "name" in dir(module) and "_cadd_features" in dir(module) and "_impute_values" in dir(module):
                self.modules.append(module)
        if len(self.modules) < 1:
            self._raise_no_module_found_error()
        self.log.info('Identified {} files available for usage in imputing.'.format(len(self.modules)))

    def _raise_no_module_found_error(self):
        """
        Function to raise when no suitable impute files are found.
        Put into a function since 2 other functions within this module will use it.
        """
        error_message = 'No usable python files are found within the imputing directory!'
        self.log.critical(error_message)
        raise FileNotFoundError(error_message)

    def _is_correct_datafile_present(self):
        """
        Function to check the CADD version and GRCh build (or --overwrite_impute_file) match the impute file.
        """
        for module in self.modules:
            if self.overrule:
                if module.name == self.overrule:
                    self.log.info('Overrule successful for: {} , located at: {}'.format(
                        self.overrule, inspect.getfile(module.__class__)))
                    self.module = module
                    break
            else:
                module_cadd_version = module.supported_cadd_version
                module_grch_build = module.supported_grch_build
                if module_cadd_version == self.cadd_version and module_grch_build == self.grch_build:
                    self.log.info('Impute data file successfully found: {} , located at: {}'.format(
                        module.name, inspect.getfile(module.__class__)))
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
        """
        Function to be called right when impute() is called, gets the cadd features and impute values from the
        impute file and saves the cadd features to the manager.
        """
        self.columns = self.module.cadd_features
        self.manager.cadd_features = self.columns
        self.impute_values = self.module.impute_values

    def impute(self, datafile: pd.DataFrame):
        """
        Function to call the CaddImputing to start imputing.
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
        """
        Function to check if all values of the columns #Chrom and Pos are present.
        :param dataset: not imputed pandas DataFrame
        :return: pandas DataFrame containing no NaN or gaps for #Chrom and Pos columns.
        """
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
        """
        Generic function to get the percentage of gaps per column
        :param dataset: not imputed pandas DataFrame
        """
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
        """
        Function to get the samples of which absolutely no prediction is possible due to all cadd feature rows being
        gaps.
        :param dataset: not imputed pandas DataFrame
        """
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
