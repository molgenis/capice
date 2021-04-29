from abc import ABCMeta, abstractmethod
from src.main.python.core.logger import Logger
from src.main.python.core.global_manager import CapiceManager
from src.main.python.resources.checkers.property_checker_logger import PropertyCheckerLogger
import pandas as pd
import numpy as np
import pickle


class TemplateSetup(metaclass=ABCMeta):
    """
    Abstract class to act as template for new models that might be
    added in future patches of CAPICE. Contains the necessary steps for preprocessing as well.
    """
    def __init__(self, name, usable, cadd_version, grch_build):
        self.log = Logger().logger
        self.property_checker = PropertyCheckerLogger()
        self.name = name
        self.usable = usable
        self.supported_cadd_version = cadd_version
        self.supported_grch_build = grch_build
        self.cadd_features = CapiceManager().cadd_features
        self.train = False
        self.model = None
        self.cadd_object = []
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
        Property setter name, to set a name for a model module. Raises TypeError if not supplied with a string.

        :param value: str
        """
        self.property_checker.check_property(value=value, expected_type=str)
        self._name = value

    @property
    def usable(self):
        """
        Property getter usable, to get the boolean value of a model module whenever it can be used for preprocessing
        and prediction.

        :return: bool
        """
        return self._usable

    @usable.setter
    def usable(self, value=False):
        """
        Property setter usable, to set the boolean value of a model module whenever it should be used for
        preprocessing and prediction. Raises TypeError if not supplied with a boolean.

        :param value: bool
        """
        self.property_checker.check_property(value=value, expected_type=bool)
        self._usable = value

    @property
    def supported_cadd_version(self):
        """
        Property getter supported_cadd_version, to get the float cadd_version value of a model/prediction file
        that is supported within the module.

        :return: float or None
        """
        return self._cadd_version

    @supported_cadd_version.setter
    def supported_cadd_version(self, value):
        """
        Property setter supported_cadd_version, to set the float cadd_version value of a model/prediction file
        that is supported within the module. Raises TypeError if not supplied with a float or None.

        :param value: float or None
        """
        self.property_checker.check_property(value=value, expected_type=float, include_none=True)
        self._cadd_version = value

    @property
    def supported_grch_build(self):
        """
        Property getter supported_grch_build, to get the integer grch_build value that defines what genome build
        is supported by the model/prediction module.

        :return: integer or None
        """
        return self._grch_build

    @supported_grch_build.setter
    def supported_grch_build(self, value):
        """
        Property getter supported_grch_build, to set the integer value grch_build that defines what genome build
        is supported by the model/prediction module. Raises TypeError if not supplied with an integer or None.

        :param value: integer or None
        """
        self.property_checker.check_property(value=value, expected_type=int, include_none=True)
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
        self.log.info('Successfully preprocessed data.')
        return processed_dataset

    def _get_categorical_columns(self, dataset: pd.DataFrame):
        """
        Function to get the categorical columns that are within the supplied CADD features of the imputing file.
        :param dataset: pandas DataFrame
        """
        for feature in dataset.select_dtypes(include=["O"]).columns:
            if feature in self.cadd_features:
                self.cadd_object.append(feature)
        self.log.debug('Converting the categorical columns: {}.'.format(", ".join(self.cadd_object)))

    @staticmethod
    def _duplicate_chr_pos_ref_alt(dataset):
        """
        Function to create the chr_pos_ref_alt column so that it doesn't get lost in preprocessing.
        :param dataset: unprocessed pandas DataFrame
        :return: unprocessed pandas DataFrame containing column 'chr_pos_ref_alt'
        """
        dataset['chr_pos_ref_alt'] = dataset[['#Chrom', 'Pos', 'Ref', 'Alt']].astype(str).agg('_'.join, axis=1)
        return dataset

    @property
    def model_features(self):
        return self._model_features

    @model_features.setter
    def model_features(self, value):
        self._model_features = value

    def _process_objects(self, dataset: pd.DataFrame):
        """
        (If train) will create a dictionary telling the processor how many categories are within a certain column. If
        not train: Will look up each CADD feature from the impute file within the columns of the datafile (either
        in full name or the column starts with the feature from the impute file). This dictionary is then passed to the
        actual processor.
        :param dataset: unprocessed pandas DataFrame
        :return: processed pandas DataFrame
        """
        cadd_feats_dict = {}
        if self.train:
            hardcoded_features = ['Ref', 'Alt', 'Domain']
            for feature in hardcoded_features:
                cadd_feats_dict[feature] = 5
            self.log.info('Training protocol, creating new categorical conversion identifiers.')
            for feat in self.cadd_object:
                if feat not in cadd_feats_dict.keys():
                    cadd_feats_dict[feat] = 5
        else:
            for feature in self.cadd_object:
                cadd_feats_dict = self._process_objects_no_train(feature=feature, cadd_features_dict=cadd_feats_dict)
        processed_data = self._process_categorical_vars(
            dataset=dataset,
            cadd_feats_dict=cadd_feats_dict
        )
        return processed_data

    def _process_objects_no_train(self, feature: str, cadd_features_dict: dict):
        for model_feature in self.model_features:
            if model_feature.startswith(feature):
                extension = model_feature.split(''.join([feature, '_']))[-1]
                if feature in cadd_features_dict.keys():
                    cadd_features_dict[feature].append(extension)
                else:
                    cadd_features_dict[feature] = [extension]
        return cadd_features_dict

    def _load_model_features(self):
        """
        Function to access the protected member of the XGBoost _Booster class to get the features that the model is
        trained on.
        :return: list
        """
        self.log.info('Using features saved within the model.')
        self.model_features = self.model._Booster.feature_names

    def _process_categorical_vars(self,
                                  dataset: pd.DataFrame,
                                  cadd_feats_dict: dict):
        """
        Processor of categorical columns. Will create new columns based on the quantity of a value within a column.
        :param dataset: unprocessed pandas DataFrame
        :param cadd_feats_dict: dictionary that is to contain the levels for each categorical feature
        :return: processed pandas DataFrame
        """
        if self.train:
            for cadd_feature in cadd_feats_dict.keys():
                feature_names = self._get_top10_or_less_cats(
                    column=dataset[cadd_feature],
                    return_num=cadd_feats_dict[cadd_feature]
                )
                dataset[cadd_feature] = np.where(dataset[cadd_feature].isin(feature_names),
                                                 dataset[cadd_feature], 'other')
        else:
            for cadd_feature in cadd_feats_dict.keys():
                feature_names = cadd_feats_dict[cadd_feature]
                self.log.debug('For feature: {} loaded {} levels: {}'.format(
                    cadd_feature,
                    len(feature_names),
                    feature_names
                ))
                dataset[cadd_feature] = np.where(dataset[cadd_feature].isin(feature_names),
                                                 dataset[cadd_feature], 'other')
        dataset = pd.get_dummies(dataset, columns=list(cadd_feats_dict.keys()))

        # Checking if all cadd features are processed. If not, add a column containing all "false" (0)
        for cadd_feature in cadd_feats_dict.keys():
            dataset = self._check_all_cadd_features_processed(
                current_cadd_feature=cadd_feature,
                dataset=dataset,
                cadd_features_dict=cadd_feats_dict
            )

        return dataset

    def _check_all_cadd_features_processed(self, current_cadd_feature, dataset: pd.DataFrame, cadd_features_dict):
        if not self.train:
            for processed_feature in cadd_features_dict[current_cadd_feature]:
                col_be_present = "_".join([current_cadd_feature, processed_feature])
                if col_be_present not in dataset.columns:
                    self.log.warning('Of CADD feature {}, detected {} not present in columns.'.format(
                        current_cadd_feature, processed_feature))
                    dataset[col_be_present] = 0
        return dataset

    def _get_top10_or_less_cats(self, column: pd.Series, return_num: int):
        """
        Function for when a training file is preprocessed to get the top return_num quantity values within a
        categorical column. Some converting is done for the logger to be able to print them.
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
        self.log.info('For feature: {} saved the following values: {}'.format(
            column.name,
            ', '.join(printable_value_counts)
        ))
        return value_counts

    # Model stuff

    def predict(self, data: pd.DataFrame):
        """
        Function to load the model and predict the CAPICE scores. Can be overwritten in case of legacy support.
        :return: pandas DataFrame
        """
        self.log.info('Predicting for {} samples.'.format(data.shape[0]))
        self._load_model()
        self._load_model_features()
        data['probabilities'] = self._predict(self._create_input_matrix(dataset=data))
        self.log.info('Predicting successful.')
        return data

    def _predict(self, predict_data):
        """
        Further down defined prediction function, which is different for XGBoost 0.72.1 and 1.1.1.
        :param predict_data: preprocessed pandas DataFrame
        :return: numpy array
        """
        return self.model.predict_proba(predict_data)[:, 1]

    def _create_input_matrix(self, dataset: pd.DataFrame):
        """
        Also a template function, which can be overwritten to be compatible with first generation CAPICE
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
            self.log.info('Successfully loaded model at: {}'.format(self._get_model_loc()))
        self.model = model

    @staticmethod
    @abstractmethod
    def _get_model_loc():
        """
        Template to mark the directory where the model is located.
        Use of os.path.join is required. You may use the get_project_root_dir() from utilities if the model is
        within this project directory.
        :return: path-like or None if no model has been created yet.
        """
        pass
