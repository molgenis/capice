from abc import ABCMeta, abstractmethod
from src.logger import Logger
from src.global_manager import CapiceManager
import pandas as pd
import numpy as np
import pickle


class TemplateSetup(metaclass=ABCMeta):
    """
    Abstract class to act as template for new models that might be
    added in future patches of CAPICE. Contains the necessary steps for preprocessing as well.
    """
    def __init__(self, name, usable, cadd_version, grch_build):
        self.log = Logger().get_logger()
        self.cadd_features = CapiceManager().get_cadd_features()
        self.train = False
        self.model = None
        self.cadd_object = []
        self.model_features = None
        self.get_name = name
        self.is_usable = usable
        self.get_supported_cadd_version = cadd_version
        self.get_supported_grch_build = grch_build

    @property
    def get_name(self):
        return self._name

    @get_name.setter
    def get_name(self, value):
        if not isinstance(value, str):
            error_message = 'Expected a string usable variable, but got {}.'.format(type(value))
            self.log.critical(error_message)
            raise TypeError(error_message)
        self._name = value

    @property
    def is_usable(self):
        return self._usable

    @is_usable.setter
    def is_usable(self, value):
        if not isinstance(value, bool):
            error_message = 'Expected a boolean usable variable, but got {}.'.format(type(value))
            self.log.critical(error_message)
            raise TypeError(error_message)
        self._usable = value

    @property
    def get_supported_cadd_version(self):
        return self._cadd_version

    @get_supported_cadd_version.setter
    def get_supported_cadd_version(self, value):
        if not isinstance(value, float):
            error_message = 'Expected a float cadd version, but got: {}.'.format(type(value))
            self.log.critical(error_message)
            raise TypeError(error_message)
        self._cadd_version = value

    @property
    def get_supported_grch_build(self):
        return self._grch_build

    @get_supported_grch_build.setter
    def get_supported_grch_build(self, value):
        if not isinstance(value, int):
            error_message = 'Expected a integer usable variable, but got {}.'.format(type(value))
            self.log.critical(error_message)
            raise TypeError(error_message)
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
            self.model_features = self._load_model_features()
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

    def _process_objects(self, dataset: pd.DataFrame):
        """
        (If train) will create a dictionary telling the processor how many categories are within a certain column. If
        not train: Will look up each CADD feature from the impute file within the columns of the datafile (either
        in full name or the column starts with the feature from the impute file). This dictionary is then passed to the
        actual processor.
        :param dataset: unprocessed pandas DataFrame
        :return: processed pandas DataFrame
        """
        cadd_feats_names_dict = {}
        cadd_feats_levels_dict = {"Ref": 5, "Alt": 5, "Domain": 5}
        if self.train:
            self.log.info('Training protocol, creating new categorical conversion identifiers.')
            for feat in self.cadd_object:
                if feat not in cadd_feats_levels_dict.keys():
                    cadd_feats_levels_dict[feat] = 5
        else:
            for feature in self.cadd_object:
                for feature_expanded_name in self.model_features:
                    if feature_expanded_name.startswith(feature):
                        expanded_name = '_'.join(feature_expanded_name.split('_')[1:])
                        if feature in cadd_feats_names_dict.keys():
                            cadd_feats_names_dict[feature].append(expanded_name)
                        else:
                            cadd_feats_names_dict[feature] = [expanded_name]
        processed_data = self._process_categorical_vars(
            dataset=dataset,
            cadd_feats_names_dict=cadd_feats_names_dict,
            cadd_feats_levels_dict=cadd_feats_levels_dict
        )
        return processed_data

    def _load_model_features(self):
        """
        Function to access the protected member of the XGBoost _Booster class to get the features that the model is
        trained on.
        :return: list
        """
        self.log.info('Using features saved within the model.')
        return self.model._Booster.feature_names

    def _process_categorical_vars(self,
                                  dataset: pd.DataFrame,
                                  cadd_feats_names_dict,
                                  cadd_feats_levels_dict):
        """
        Processor of categorical columns. Will create new columns based on the quantity of a value within a column.
        :param dataset: unprocessed pandas DataFrame
        :param cadd_feats_names_dict: dictionary that is used when it is not preprocessing a training file
        :param cadd_feats_levels_dict: dictionary that is used when processing a training file
        :return: processed pandas DataFrame
        """
        if self.train:
            for cadd_feat in cadd_feats_levels_dict.keys():
                feature_names = self._get_top10_or_less_cats(
                    column=dataset[cadd_feat],
                    return_num=cadd_feats_levels_dict[cadd_feat]
                )
                dataset[cadd_feat] = np.where(dataset[cadd_feat].isin(feature_names),
                                              dataset[cadd_feat], 'other')
        else:
            for cadd_feat in cadd_feats_names_dict.keys():
                feature_names = cadd_feats_names_dict[cadd_feat]
                self.log.debug('For feature: {} loaded {} levels.'.format(
                    cadd_feat,
                    len(feature_names)
                ))
                dataset[cadd_feat] = np.where(dataset[cadd_feat].isin(feature_names),
                                              dataset[cadd_feat], 'other')
        dataset = pd.get_dummies(dataset, columns=self.cadd_object)
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

    def get_model_features(self):
        """
        Function to be called by external modules to export the CADD features used in the model.
        :return: list
        """
        return self.model_features

    # Model stuff

    def predict(self, data: pd.DataFrame):
        """
        Function to load the model and predict the CAPICE scores. Can be overwritten in case of legacy support.
        :return: pandas DataFrame
        """
        self.log.info('Predicting for {} samples.'.format(data.shape[0]))
        self._load_model()
        self.model_features = self._load_model_features()
        data['probabilities'] = self._predict(self._create_input_matrix(dataset=data))
        data['ID'] = '.'
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
            model = pickle.load(open(self._get_model_loc(), 'rb'))
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
