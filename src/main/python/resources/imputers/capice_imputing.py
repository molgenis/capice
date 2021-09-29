from src.main.python.core.logger import Logger
import inspect
import numpy as np
from src.main.python.resources.utilities.utilities import \
    get_project_root_dir, load_modules, importer, deprecated
from src.main.python.core.global_manager import CapiceManager
import pandas as pd
import os


class CapiceImputing:
    """
    Class to dynamically load in all imputing files and identify the file
    suitable for the run's use case.
    """

    def __init__(self):
        self.manager = CapiceManager()
        self.vep_version = self.manager.vep_version
        self.grch_build = self.manager.grch_build
        self.log = Logger().logger
        self.log.info('Imputer started.')
        self.overrule = self.manager.overwrite_impute
        self.modules = []
        self.module = None
        self._load_modules()
        self._is_correct_datafile_present()
        self._check_if_imputer_is_applied()
        self.columns = []
        self.annotation_columns_present = []
        self.impute_values = {}
        self.pre_dtypes = {}
        self.dtypes = {}

    def _load_modules(self):
        """
        Method to dynamically load in all python files containing a class that
        contains the properties
            name and
            _json_name.
        If at the end of this function, the list of impute files is empty,
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
            if "name" in dir(module) and "_json_name" in dir(module):
                self.modules.append(module)
        if len(self.modules) < 1:
            self._raise_no_module_found_error()
        self.log.info(
            'Identified %s files available for usage in imputing.',
            len(self.modules)
        )

    def _raise_no_module_found_error(self):
        """
        Function to raise when no suitable impute files are found.
        Put into a function since 2 other functions within this module will use
        it.
        """
        error_message = 'No usable python files are found ' \
                        'within the imputing directory!'
        self.log.critical(error_message)
        raise FileNotFoundError(error_message)

    def _is_correct_datafile_present(self):
        """
        Function to check the VEP version and GRCh build
        (or --overwrite_impute_file)
        match the impute file.
        """
        for module in self.modules:
            if self.overrule and module.name == self.overrule:
                self.log.info(
                    'Overrule successful for: %s, located at: %s',
                    self.overrule,
                    inspect.getfile(module.__class__)
                )
                self.module = module
                break
            else:
                module_vep_version = module.supported_vep_version
                module_grch_build = module.supported_grch_build
                if module_vep_version == self.vep_version and \
                        module_grch_build == self.grch_build:
                    self.log.info(
                        'Impute data file successfully found: %s, '
                        'located at: %s', module.name,
                        inspect.getfile(module.__class__)
                    )
                    self.module = module
                    break

    def _check_if_imputer_is_applied(self):
        # Checking if self.data_file is assigned
        if self.module is None:
            if self.overrule:
                error_message = 'No imputing data file found for overrule: ' \
                                '{}'.format(self.overrule)
            else:
                error_message = 'No imputing data file found for ' \
                                'VEP version: {} and ' \
                                'GRCh build: {}'.format(self.vep_version,
                                                        self.grch_build
                                                        )
            self.log.critical(error_message)
            raise FileNotFoundError(error_message)

    def _load_values(self, dataset: pd.DataFrame):
        """
        Function to be called right when impute() is called,
        gets the input datafile features,
        imputes values from the impute file and
        saves the datafile features to the manager.
        """
        self.columns = self.module.annotation_features
        for col in self.columns:
            if col in dataset.columns:
                self.annotation_columns_present.append(col)
            else:
                self.log.debug('Annotation feature %s not present within '
                               'input data!', col)
        self.manager.annotation_features = self.annotation_columns_present
        self.impute_values = self.module.impute_values

    def impute(self, datafile: pd.DataFrame):
        """
        Function to call the CapiceImputing to start imputing.
        :return: pandas DataFrame
        """
        self._load_values(datafile)
        datafile = self._check_chrom_pos(datafile)
        self._get_nan_ratio_per_column(dataset=datafile)
        self._get_full_nan_row(dataset=datafile)
        datafile.dropna(how='all', subset=self.annotation_columns_present)
        datafile = datafile[~datafile['CAPICE_drop_out']]
        datafile.drop(columns=['CAPICE_drop_out'], inplace=True)
        self._correct_dtypes(datafile=datafile)
        datafile.fillna(self.impute_values, inplace=True)
        datafile = datafile.astype(dtype=self.pre_dtypes, copy=False)
        datafile = datafile.astype(dtype=self.dtypes, copy=False)
        self.log.info('Imputing successfully performed.')
        return datafile

    def _correct_dtypes(self, datafile: pd.DataFrame):
        """
        Function to correct the dtypes that originate from the lookup annotator
        according to the dtypes specified within the data json.
        """
        for key, item in self.impute_values.items():
            if key in datafile.columns:
                self._save_dtypes(key=key, item=item)

    def _save_dtypes(self, key, item):
        if isinstance(item, int):
            self.pre_dtypes[key] = float
        else:
            self.pre_dtypes[key] = type(item)
        self.dtypes[key] = type(item)

    def _check_chrom_pos(self, dataset: pd.DataFrame):
        """
        Function to check if all values of the columns Chr and Pos are present.
        :param dataset: not imputed pandas DataFrame
        :return: pandas DataFrame
            containing no NaN or gaps for Chr and Pos columns.
        """
        chrom_is_float = False
        if dataset['Chr'].isnull().values.any():
            if dataset.dtypes['Chr'] == np.float64:
                chrom_is_float = True
            n_delete = dataset['Chr'].isnull().values.sum()
            self.log.warning(
                'Detected NaN in the Chromosome column! '
                'Deleting %s row(s).', n_delete)
            dataset = dataset[~dataset['Chr'].isnull()]
        if dataset['Pos'].isnull().values.any():
            n_delete = dataset['Pos'].isnull().values.sum()
            self.log.warning(
                'Detected NaN is the Position column! '
                'Deleting %s row(s).', n_delete)
            dataset = dataset[~dataset['Pos'].isnull()]
        dataset.index = range(0, dataset.shape[0])
        if chrom_is_float:
            dataset['Chr'] = dataset['Chr'].astype(int)
            dataset['Chr'] = dataset['Chr'].astype(str)
        dataset['Pos'] = dataset['Pos'].astype(int)
        return dataset

    def _get_nan_ratio_per_column(self, dataset: pd.DataFrame):
        """
        Generic function to get the percentage of gaps per column
        :param dataset: not imputed pandas DataFrame
        """
        for column in dataset.columns:
            series = dataset[column]
            self._calculate_percentage_nan(column=series)

    def _calculate_percentage_nan(self, column):
        n_nan = column.isnull().sum()
        if n_nan > 0:
            n_samples = column.size
            p_nan = round((n_nan / n_samples) * 100, ndigits=2)
            self.log.debug('NaN detected in column %s, percentage: %s%%.',
                           column.name,
                           p_nan
                           )

    def _get_full_nan_row(self, dataset: pd.DataFrame):
        """
        Function to get the samples of which absolutely no prediction is
        possible due to all non chr pos ref alt rows being gaps.
        :param dataset: not imputed pandas DataFrame
        """
        n_samples = dataset.shape[0]
        dataset.index = range(1, n_samples + 1)
        dataset['CAPICE_drop_out'] = dataset[
            self.annotation_columns_present].isnull().values.all(
            axis=1)
        samples_dropped_out = dataset[dataset['CAPICE_drop_out']]
        if samples_dropped_out.shape[0] > 0:
            self.log.warning(
                'The following samples are filtered out due to missing values: '
                '(indexing is python based, '
                'so the index starts at 0). \n %s',
                samples_dropped_out[
                    ['Chr', 'Pos', 'Ref', 'Alt', 'FeatureID']]
            )
        else:
            self.log.info(
                'No samples are filtered out due to too many NaN values.')
