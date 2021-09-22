from abc import ABCMeta, abstractmethod
import logging
logger = logging.getLogger(__name__)
from src.main.python.core.global_manager import CapiceManager
from src.main.python.resources.checkers.property_checker_logger import \
    PropertyCheckerLogger
from src.main.python.resources.utilities.utilities import deprecated
from src.main.python.resources.enums.sections import Column
import pandas as pd
import numpy as np
import pickle


class TemplateSetup(metaclass=ABCMeta):
    """
    Abstract class to act as template for new models that might be
    added in future patches of CAPICE.
    Contains the necessary steps for preprocessing as well.
    """

    def __init__(self, name, usable, vep_version, grch_build):
        self.property_checker = PropertyCheckerLogger()
        self.name = name
        self.usable = usable
        self.supported_vep_version = vep_version
        self.supported_grch_build = grch_build
        self.annotation_features = CapiceManager().annotation_features
        self.train = False
        self.model = None
        self.annotation_object = []
        self.model_features = None

    @property
    def name(self):
        """
        Property getter name, to get the init defined name of the model module.

        :return: str
        """
        return self._name

    @name.setter
    def name(self, value='Template'):
        """
        Property setter name, to set a name for a model module.
        Raises TypeError if not supplied with a string.

        :param value: str
        """
        self.property_checker.check_property(value=value, expected_type=str)
        self._name = value

    @property
    def usable(self):
        """
        Property getter usable, to get the boolean value of a model module
        whenever it can be used for preprocessing and prediction.

        :return: bool
        """
        return self._usable

    @usable.setter
    def usable(self, value=False):
        """
        Property setter usable, to set the boolean value of a model module
        whenever it should be used for preprocessing and prediction.
        Raises TypeError if not supplied with a boolean.

        :param value: bool
        """
        self.property_checker.check_property(value=value, expected_type=bool)
        self._usable = value

    @property
    def supported_vep_version(self):
        """
        Property getter supported_annotation_version,
        to get the float annotation_version value of a model/prediction file
        that is supported within the module.

        :return: float or None
        """
        return self._vep_version

    @supported_vep_version.setter
    def supported_vep_version(self, value):
        """
        Property setter supported_annotation_version,
        to set the float annotation_version value of a model/prediction file
        that is supported within the module.
        Raises TypeError if not supplied with a float or None.

        :param value: float or None
        """
        self.property_checker.check_property(
            value=value,
            expected_type=float,
            include_none=True
        )
        self._vep_version = value

    @property
    def supported_grch_build(self):
        """
        Property getter supported_grch_build,
        to get the integer grch_build value that defines what genome build
        is supported by the model/prediction module.

        :return: integer or None
        """
        return self._grch_build

    @supported_grch_build.setter
    def supported_grch_build(self, value):
        """
        Property getter supported_grch_build,
        to set the integer value grch_build that defines what genome build
        is supported by the model/prediction module.
        Raises TypeError if not supplied with an integer or None.

        :param value: integer or None
        """
        self.property_checker.check_property(
            value=value,
            expected_type=int,
            include_none=True
        )
        self._grch_build = value

    def preprocess(self, dataset: pd.DataFrame, is_train: bool):
        """
        Callable function to start the preprocessing of a dataset.
        :param dataset: imputed pandas DataFrame
        :param is_train: boolean
        :return: processed pandas DataFrame
        """
        self.train = is_train
        self._load_model()
        if not self.train:
            self._load_model_features()
        dataset = self._duplicate_chr_pos_ref_alt(dataset=dataset)
        self._get_categorical_columns(dataset=dataset)
        processed_dataset = self._process_objects(dataset=dataset)
        if not self.train:
            processed_dataset = self._check_all_model_features_present(
                processed_dataset
            )
        logger.info('Successfully preprocessed data.')
        return processed_dataset

    @deprecated
    def _check_all_model_features_present(self, dataset: pd.DataFrame):
        for feature in self.model_features:
            if feature not in dataset.columns:
                dataset[feature] = 0
        return dataset

    def _get_categorical_columns(self, dataset: pd.DataFrame):
        """
        Function to get the categorical columns that are within the supplied
        annotation features of the imputing file.
        :param dataset: pandas DataFrame
        """
        for feature in dataset.select_dtypes(include=["O"]).columns:
            if feature in self.annotation_features:
                self.annotation_object.append(feature)
        logger.debug(
            'Converting the categorical columns: %s.', ", ".join(self.annotation_object)
        )

    @staticmethod
    def _duplicate_chr_pos_ref_alt(dataset):
        """
        Function to create the chr_pos_ref_alt column so that it doesn't get
        lost in preprocessing.
        :param dataset: unprocessed pandas DataFrame
        :return: unprocessed pandas DataFrame
            containing column 'chr_pos_ref_alt'
        """
        dataset['chr_pos_ref_alt'] = dataset[
            ['Chr', 'Pos', 'Ref', 'Alt']].astype(str).agg('_'.join, axis=1)
        return dataset

    @property
    def model_features(self):
        return self._model_features

    @model_features.setter
    def model_features(self, value):
        self._model_features = value

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
            hardcoded_features = ['Ref', 'Alt', 'Domain']
            for feature in hardcoded_features:
                annotation_feats_dict[feature] = 5
            logger.info(
                'Training protocol, '
                'creating new categorical conversion identifiers.'
            )
            for feat in self.annotation_object:
                if feat not in annotation_feats_dict.keys():
                    annotation_feats_dict[feat] = 5
        else:
            for feature in self.annotation_object:
                annotation_feats_dict = self._process_objects_no_train(
                    feature=feature,
                    annotation_features_dict=annotation_feats_dict
                )
        processed_data = self._process_categorical_vars(
            dataset=dataset,
            annotation_feats_dict=annotation_feats_dict
        )
        return processed_data

    def _process_objects_no_train(self, feature: str,
                                  annotation_features_dict: dict):
        for model_feature in self.model_features:
            if model_feature.startswith(feature):
                extension = model_feature.split(''.join([feature, '_']))[-1]
                if feature in annotation_features_dict.keys():
                    annotation_features_dict[feature].append(extension)
                else:
                    annotation_features_dict[feature] = [extension]
        return annotation_features_dict

    def _load_model_features(self):
        """
        Function to access the protected member of the XGBoost _Booster class
        to get the features that the model is trained on.
        :return: list
        """
        logger.info('Using features saved within the model.')
        self.model_features = self.model.get_booster().feature_names

    def _process_categorical_vars(self,
                                  dataset: pd.DataFrame,
                                  annotation_feats_dict: dict):
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
                feature_names = self._get_top10_or_less_cats(
                    column=dataset[annotation_feature],
                    return_num=annotation_feats_dict[annotation_feature]
                )
                dataset[annotation_feature] = np.where(
                    dataset[annotation_feature].isin(feature_names),
                    dataset[annotation_feature],
                    'other')
        else:
            for annotation_feature in annotation_feats_dict.keys():
                feature_names = annotation_feats_dict[annotation_feature]
                logger.debug('For feature: %s loaded %s levels: %s',
                    annotation_feature,
                    len(feature_names),
                    feature_names
                )
                dataset[annotation_feature] = np.where(
                    dataset[annotation_feature].isin(feature_names),
                    dataset[annotation_feature],
                    'other'
                )
        dataset = pd.get_dummies(
            dataset,
            columns=list(annotation_feats_dict.keys())
        )

        # Checking if all annotation features are processed.
        # If not, add a column containing all "false" (0)
        for annotation_feature in annotation_feats_dict.keys():
            dataset = self._check_all_annotation_features_processed(
                current_annotation_feature=annotation_feature,
                dataset=dataset,
                annotation_features_dict=annotation_feats_dict
            )

        return dataset

    def _check_all_annotation_features_processed(self,
                                                 current_annotation_feature,
                                                 dataset: pd.DataFrame,
                                                 annotation_features_dict):
        if not self.train:
            afd = annotation_features_dict
            for processed_feature in afd[current_annotation_feature]:
                col_be_present = "_".join(
                    [current_annotation_feature, processed_feature])
                if col_be_present not in dataset.columns:
                    logger.warning(
                        'Of annotation feature %s,'
                        ' detected %s not present in columns.',
                            current_annotation_feature, processed_feature)
                    dataset[col_be_present] = 0
        return dataset

    def _get_top10_or_less_cats(self, column: pd.Series, return_num: int):
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
        logger.info('For feature: %s saved the following values: %s',
            column.name,
            ', '.join(printable_value_counts)
        )
        return value_counts

    # Model stuff

    def predict(self, data: pd.DataFrame):
        """
        Function to load the model and predict the CAPICE scores.
        Can be overwritten in case of legacy support.
        :return: pandas DataFrame
        """
        logger.info('Predicting for %s samples.', data.shape[0])
        self._load_model()
        self._load_model_features()
        data[Column.score.value] = self._predict(
            self._create_input_matrix(dataset=data))
        logger.info('Predicting successful.')
        return data

    def _predict(self, predict_data):
        """
        Further down defined prediction function, which is different for
        XGBoost 0.72.1 and current XGBoost version.
        :param predict_data: preprocessed pandas DataFrame
        :return: numpy array
        """
        return self.model.predict_proba(predict_data)[:, 1]

    def _create_input_matrix(self, dataset: pd.DataFrame):
        """
        Also a template function, which can be overwritten to be compatible
        with first generation CAPICE.
        :param dataset: pandas DataFrame
        :return: XGBoost workable data
        """
        return dataset[self.model_features]

    def _load_model(self):
        """
        Template method to load in the model once supported values are correct.
        :return: pickled model instance
        """
        model = None
        if not self.train:
            with open(self._get_model_loc(), 'rb') as model_file:
                model = pickle.load(model_file)
            logger.info('Successfully loaded model at: %s',
                self._get_model_loc())
        self.model = model

    @staticmethod
    @abstractmethod
    def _get_model_loc():
        """
        Template to mark the directory where the model is located.
        Use of os.path.join is required.
        You may use the get_project_root_dir() from utilities if the model is
        within this project directory.
        :return: path-like or None if no model has been created yet.
        """
        pass
