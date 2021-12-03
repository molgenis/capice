import pandas as pd

from src.main.python.core.logger import Logger
from src.main.python.utilities.enums import Column


class CapiceImputing:
    """
    Class to perform the imputing on a fully VEP processed pandas dataframe.
    """

    def __init__(self, impute_values: dict):
        """
        :param impute_values: dict, Dictionary containing all features to be
        imputed as keys and the fill value as value. Can come from either the
        model or a loaded json.
        """
        self.log = Logger().logger
        self.log.info('Imputer started.')
        self.impute_values = impute_values
        self.pre_dtypes = {}
        self.dtypes = {}

    def impute(self, datafile: pd.DataFrame):
        """
        Function to call the CapiceImputing to start imputing.
        :return: pandas DataFrame
        """
        # Get the amount of NaN per column
        self._get_nan_ratio_per_column(dataset=datafile)

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
        # First, correct the Chromosome column, then the rest.
        datafile[Column.chr.value] = datafile[Column.chr.value].astype(str)
        for key, item in self.impute_values.items():
            if key in datafile.columns:
                # Required, see pydoc of _save_dtypes()
                self._save_dtypes(key=key, item=item)

    def _save_dtypes(self, key, item):
        """
        Pre-dtypes are required since converting to an integer requires a float
        """
        if isinstance(item, int):
            self.pre_dtypes[key] = float
        else:
            self.pre_dtypes[key] = type(item)
        self.dtypes[key] = type(item)

    def _get_nan_ratio_per_column(self, dataset: pd.DataFrame):
        """
        Generic function to get the percentage of gaps per column
        :param dataset: not imputed pandas DataFrame
        """
        for column in dataset.columns:
            series = dataset[column]
            self._calculate_percentage_nan(column=series)

    @staticmethod
    def _calculate_percentage(value, total):
        return round((value / total) * 100, ndigits=2)

    def _calculate_percentage_nan(self, column):
        n_nan = column.isnull().sum()
        if n_nan > 0:
            n_samples = column.size
            p_nan = self._calculate_percentage(n_nan, n_samples)
            self.log.debug('NaN detected in column %s, percentage: %s%%.', column.name, p_nan)
