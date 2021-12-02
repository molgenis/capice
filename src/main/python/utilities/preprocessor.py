import numpy as np
import pandas as pd

from src.main.python.core.logger import Logger
from src.main.python.utilities.enums import Column, UniqueSeparator
from src.main.python.core.capice_manager import CapiceManager


class PreProcessor:
    """
    Class to preprocess the data before predicting or training to separate
    categorical columns.
    """

    def __init__(self, exclude_features: list, model_features: list = None):
        """
        :param exclude_features: list,
            all the features that the preprocessor should not process.
        Features that are already excluded include:
            chr_pos_ref_alt, chr and pos.
        :param model_features: list (default None), a list containing all
        the features present within a model file.
        """
        self.log = Logger().logger
        self.manager = CapiceManager()
        self.log.info('Preprocessor started.')
        self.train = False
        self.exclude_features = [
            Column.chr_pos_ref_alt.value,
            Column.chr.value,
            Column.pos.value
        ]
        self.exclude_features += exclude_features
        self.model_features = model_features
        self.objects = []

    def _is_train(self):
        if self.model_features is None:
            self.train = True

    def preprocess(self, dataset: pd.DataFrame):
        """
        Callable function for the preprocessor to start preprocessing.
        :param dataset: unprocessed pandas DataFrame
        :return: processed pandas Dataframe
        """
        self._is_train()
        dataset = self._create_preservation_col(dataset)
        self._get_categorical_columns(dataset)
        processed_dataset = self._process_objects(dataset)
        if not self.train:
            processed_dataset = self._ensure_columns_present(processed_dataset)
        self.log.info('Successfully preprocessed data.')
        return processed_dataset

    @staticmethod
    def _create_preservation_col(dataset):
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
        return dataset

    def _get_categorical_columns(self, dataset: pd.DataFrame):
        """
        Function to get the categorical columns that are within the supplied
        annotation features of the imputing file.
        :param dataset: pandas DataFrame
        """
        for feature in dataset.select_dtypes(include=["O"]).columns:
            if feature not in self.exclude_features:
                self.objects.append(feature)
        self.log.debug('Converting the categorical columns: %s.', ', '.join(self.objects))

    def _process_objects(self, dataset: pd.DataFrame):
        """
        (If train) will create a dictionary telling the processor how many
        categories are within a certain column.
        If not train: Will look up each annotation feature from the impute file
        within the columns of the datafile (either in full name or the column
        starts with the feature from the impute file).
        This dictionary is then passed to the actual processor.
        :param dataset: unprocessed pandas DataFrame
        :return: processed pandas DataFrame
        """
        annotation_feats_dict = {}
        if self.train:
            hardcoded_features = [Column.ref.value, Column.alt.value, 'Domain']
            for feature in hardcoded_features:
                annotation_feats_dict[feature] = 5
            self.log.info('Training protocol, creating new categorical conversion identifiers.')
            for feat in self.objects:
                if feat not in annotation_feats_dict.keys():
                    annotation_feats_dict[feat] = 5
        else:
            for feature in self.objects:
                annotation_feats_dict = self._process_objects_no_train(
                    feature=feature,
                    annotation_features_dict=annotation_feats_dict
                )
        processed_data = self._process_categorical_vars(
            dataset=dataset,
            annotation_feats_dict=annotation_feats_dict
        )
        return processed_data

    def _process_objects_no_train(self, feature: str, annotation_features_dict: dict):
        for model_feature in self.model_features:
            if model_feature.startswith(feature):
                extension = model_feature.split(''.join([feature, '_']))[-1]
                if feature in annotation_features_dict.keys():
                    annotation_features_dict[feature].append(extension)
                else:
                    annotation_features_dict[feature] = [extension]
        return annotation_features_dict

    def _process_categorical_vars(self, dataset: pd.DataFrame, annotation_feats_dict: dict):
        """
        Processor of categorical columns. Will create new columns based on the
        quantity of a value within a column.
        :param dataset: unprocessed pandas DataFrame
        :param annotation_feats_dict:
            dictionary that is to contain the levels for each categorical
            feature
        :return: processed pandas DataFrame
        """
        if self.train:
            for annotation_feature in annotation_feats_dict.keys():
                feature_names = self._get_top_n_cats(
                    column=dataset[annotation_feature],
                    return_num=annotation_feats_dict[annotation_feature]
                )
                dataset[annotation_feature] = np.where(
                    dataset[annotation_feature].isin(feature_names),
                    dataset[annotation_feature],
                    'other'
                )
        else:
            for annotation_feature in annotation_feats_dict.keys():
                feature_names = annotation_feats_dict[annotation_feature]
                self.log.debug('For feature: %s loaded %s levels: %s',
                               annotation_feature,
                               len(feature_names),
                               feature_names
                               )
                dataset[annotation_feature] = np.where(
                    dataset[annotation_feature].isin(feature_names),
                    dataset[annotation_feature],
                    'other'
                )
        dataset = pd.get_dummies(dataset, columns=list(annotation_feats_dict.keys()))

        return dataset

    def _get_top_n_cats(self, column: pd.Series, return_num: int):
        """
        Function for when a training file is preprocessed to get the top
        return_num quantity values within a categorical column.
        Some converting is done for the logger to be able to print them.
        :param column: pandas Series
        :param return_num: integer
        :return: pandas Series
        """
        value_counts = column.value_counts().index[:return_num].values
        printable_value_counts = []
        for value in value_counts:
            if not isinstance(value, str):
                value = str(value)
            printable_value_counts.append(value)
        message = 'For feature: %s saved the following values: %s'
        self.log.info(message, column.name, ', '.join(printable_value_counts))
        return value_counts

    def _ensure_columns_present(self, dataset):
        """
        Function to ensure that for the prediction all prediction columns
        are present. If a columns is not present, add it with a full
        columns of NaN.
        """
        for feature in self.model_features:
            if feature not in dataset.columns:
                message = 'Detected column %s not present in columns. Adding full column of NaN'
                self.log.debug(message, feature)
                dataset[feature] = np.nan
        return dataset
