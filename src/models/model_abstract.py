from abc import ABCMeta, abstractmethod
from src.logger import Logger
from src.global_manager import CapiceManager
import pandas as pd
import numpy as np
import pickle
import xgboost as xgb


class ModelSetup(metaclass=ABCMeta):
    """
    Abstract class to act as template for new models that might be
    added in future patches of CAPICE.
    """
    def __init__(self):
        self.log = Logger().get_logger()
        self.cadd_features = CapiceManager().get_cadd_features()
        self.train = False
        self.model = None
        self.cadd_object = []
        self.model_features = []

    # Preprocessing stuff

    @staticmethod
    @abstractmethod
    def get_name():
        return "Template"

    def preprocess(self, dataset: pd.DataFrame, is_train: bool):
        self.train = is_train
        self._load_model()
        self._get_categorical_columns(dataset=dataset)
        processed_dataset = self._process_objects(dataset=dataset)
        return processed_dataset

    def _get_categorical_columns(self, dataset: pd.DataFrame):
        for feature in dataset.select_dtypes(include=["O"]).columns:
            if feature in self.cadd_features:
                self.cadd_object.append(feature)
        self.log.info('Converting the categorical columns: {}.'.format(", ".join(self.cadd_object)))

    def _process_objects(self, dataset: pd.DataFrame):
        cadd_feats_names_dict = {}
        cadd_feats_levels_dict = {"Ref": 5, "Alt": 5, "Domain": 5}
        if self.train:
            self.log.info('Training protocol, creating new categorical conversion identifiers.')
            for feat in self.cadd_object:
                if feat not in cadd_feats_levels_dict.keys():
                    cadd_feats_levels_dict[feat] = 5
        else:
            model_features = self._load_model_features()
            for feature in self.cadd_object:
                for feature_expanded_name in model_features:
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
        self.log.info('Using features saved within the model.')
        return self.model._Booster.feature_names

    def _process_categorical_vars(self,
                                  dataset: pd.DataFrame,
                                  cadd_feats_names_dict,
                                  cadd_feats_levels_dict):
        for cadd_feat in cadd_feats_levels_dict.keys():
            if self.train:
                feature_names = self._get_top10_or_less_cats(
                    column=dataset[cadd_feat],
                    return_num=cadd_feats_levels_dict[cadd_feat]
                )
            else:
                feature_names = cadd_feats_names_dict[cadd_feat]
                self.log.info('For feature: {} loaded {} levels.'.format(
                    cadd_feat,
                    len(feature_names)
                ))
            dataset[cadd_feat] = np.where(dataset[cadd_feat].isin(feature_names),
                                          dataset[cadd_feat], 'other')
        dataset = pd.get_dummies(dataset, columns=self.cadd_object)
        self.log.info('Successfully processed categorical values.')
        return dataset

    def _get_top10_or_less_cats(self, column: pd.Series, return_num: int):
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

    @staticmethod
    @abstractmethod
    def get_supported_cadd_version():
        """
        Template for the model setup to tell CAPICE
        what CADD version is supported.
        :return: float
        """
        return None

    @staticmethod
    @abstractmethod
    def get_supported_genomebuild_version():
        """
        Template for the model setup to tell CAPICE what genome build is
        supported.
        :return: int
        """
        return None

    def predict(self, data: pd.DataFrame):
        """
        Template method for a model setup to predict and return scores.
        :return: pandas DataFrame
        """
        self.log.info('Predicting for {} samples.'.format(data.shape[0]))
        data['probabilities'] = self._predict(self._create_input_matrix(data))
        data['ID'] = '.'
        return data

    def _predict(self, predict_data):
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
        if not self.train:
            model = pickle.load(open(self._get_model_loc(), 'rb'))
            self.log.info('Successfully loaded model at: {}'.format(self._get_model_loc()))
            return model
        else:
            return None

    @staticmethod
    @abstractmethod
    def _get_model_loc():
        """
        Template to mark the directory where the model is located.
        Use of os.path.join is required. You may use the get_project_root_dir() from utilities if the model is
        within this project directory.
        :return: path-like or None if no model has been created yet.
        """
        return ""
