import numpy as np
import pandas as pd

from molgenis.capice.core.logger import Logger
from molgenis.capice.core.capice_manager import CapiceManager
from molgenis.capice.utilities.column_utils import ColumnUtils
from molgenis.capice.utilities.enums import Column, UniqueSeparator


class CategoricalProcessor:
    """
    Class to process the data before predicting or training to separate
    categorical columns.
    """

    def __init__(self):
        self.log = Logger().logger
        self.manager = CapiceManager()

    def process(
            self,
            dataset: pd.DataFrame,
            processable_features: list[str] | None = None,
            predetermined_features: dict[str, list] | None = None
    ) -> tuple[pd.DataFrame, dict[str, list]]:
        """
        Callable method of CategoricalProcessor to start processing the categorical columns
        of dataset according to either processable_features (in case of train) or
        predetermined_features (in case of predict).

        Args:
            dataset:
                The dataset over which the categorical features should be processed.
            processable_features:
                list of processable train features that this module limits to.
                If used in predict: set to None.
            predetermined_features:
                Dictionary of features as they are put into the CategoricalProcessor (key) and
                the features they should end up being (values).
                If used in train: set to None.
        Returns:
            processed_dataset:
                Dataset with all "Other" dtype columns processed to new columns that have either
                0 or 1 depending on if that sample had the categorical feature or not.
            processing_features:
                Dictionary containing the columns (key) and the columns they turned into as
                output (values).
        Raises:
            ValueError:
                ValueError is raised when both processable_features and predetermined_features
                are set to None.
        """
        self.log.info('Starting processing categorical columns.')
        self._validate_one_feature_list_present(processable_features, predetermined_features)
        self._create_preservation_col(dataset)
        if predetermined_features is None:
            # Type ignore, else mypy takes issue with Typing since processable_features can be
            # None, so it is considered Optional[list[str]] instead of list[str].
            processing_features = self._get_categorical_columns(
                dataset,
                processable_features  # type: ignore
            )
        else:
            processing_features = predetermined_features

        processed_dataset = self._get_dummies(dataset, processing_features)

        self._ensure_columns_present(processed_dataset, processing_features)

        self.log.info('Successfully processed categorical data.')
        return processed_dataset, processing_features

    def _validate_one_feature_list_present(
            self,
            processable_features: list | None,
            predetermined_features: dict[str, list] | None
    ) -> None:
        if processable_features is None and predetermined_features is None:
            error_message = 'Both processable_features and predetermined_features are not supplied!'
            self.log.critical(error_message)
            raise ValueError(error_message)

    @staticmethod
    def _create_preservation_col(dataset: pd.DataFrame) -> None:
        """
        Function to create the chr_pos_ref_alt column so that it doesn't get
        lost in preprocessing.
        :param dataset: unprocessed pandas DataFrame
        :return: unprocessed pandas DataFrame
            containing column 'chr_pos_ref_alt'
        """
        dataset[Column.chr_pos_ref_alt.value] = dataset[
            [Column.chr.value, Column.pos.value, Column.ref.value, Column.alt.value]
        ].astype(str).agg(UniqueSeparator.unique_separator.value.join, axis=1)

    def _get_categorical_columns(self, dataset: pd.DataFrame,
                                 processable_features: list[str]) -> dict[str, list]:
        """
        Method for when the predetermined_features is None, usually in case of train,
        to determine the top 5 features that should be used for pandas.get_dummies().
        Loops through the "Object" dtype features in dataset, and if the feature is in the
        processable_features list it will obtain the most common values of the feature.
        """
        processing_features = {}
        for feature in dataset.select_dtypes(include=["O"]).columns:
            if feature in processable_features:
                self.log.debug('Converting the categorical column: %s', feature)
                processing_features[feature] = self._process_object(dataset[feature])
        return processing_features

    def _process_object(self, feature_column: pd.Series) -> list:
        """
        Method to call the top X categories method with return number 5
        """
        top_categories = self._get_top_n_cats(feature_column, return_num=5)
        return top_categories

    def _get_top_n_cats(self, column: pd.Series, return_num: int) -> list:
        """
        Function for when a training file is preprocessed to get the top
        return_num quantity values within a categorical column.
        Some converting is done for the logger to be able to print them.
        :param column: pandas Series
        :param return_num: integer
        :return: pandas Series
        """
        counts = column.value_counts().index
        value_counts = list(counts[:return_num])
        if len(counts) > return_num:
            value_counts.append(Column.other.value)
        message = 'For feature: %s saved the following values: %s'
        self.log.info(message, column.name, ', '.join(value_counts))
        return value_counts

    def _get_dummies(self, dataset: pd.DataFrame, processing_features: dict) -> pd.DataFrame:
        """
        Method to call the pandas.get_dummies() method to convert categorical into multiple columns
        of 0 and 1.
        """
        for feature, feature_values in processing_features.items():
            self._set_other_values(dataset, feature, feature_values)
        processed_dataset = pd.get_dummies(dataset, columns=processing_features.keys())
        return processed_dataset

    def _set_other_values(self, dataset: pd.DataFrame, feature_name: str, feature_values: list) -> \
            None:
        """
        Method to set all other entries within a column to "other" if they are not in
        feature_values list.
        """
        self.log.debug(
            'Converting %d features for feature: %s : %s',
            len(feature_values),
            feature_name,
            ", ".join(feature_values)
        )
        dataset[feature_name] = np.where(
            dataset[feature_name].isin(feature_values),
            dataset[feature_name],
            Column.other.value
        )

    def _ensure_columns_present(self, dataset: pd.DataFrame, categorical_out_columns: dict) -> None:
        merged_columns = []
        for main_feature, derivative_features in categorical_out_columns.items():
            for feature in derivative_features:
                merged_columns.append(f'{main_feature}_{feature}')
        column_utils = ColumnUtils()
        column_utils.set_specified_columns(merged_columns)
        missing = column_utils.get_missing_diff_with(dataset.columns)
        for feature in missing:
            message = 'Detected column %s not present in columns. Adding full column on NaN'
            self.log.debug(message, feature)
            dataset[feature] = np.nan
