from abc import ABCMeta, abstractmethod
from src.logger import Logger
from src.global_manager import CapiceManager
import pandas as pd
import numpy as np
import pickle


class TemplateSetup(metaclass=ABCMeta):
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
        self.model_features = None

    @staticmethod
    @abstractmethod
    def get_name():
        return 'Template'

    @staticmethod
    @abstractmethod
    def is_usable():
        return False

    def preprocess(self, dataset: pd.DataFrame, is_train: bool):
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
        for feature in dataset.select_dtypes(include=["O"]).columns:
            if feature in self.cadd_features:
                self.cadd_object.append(feature)
        self.log.debug('Converting the categorical columns: {}.'.format(", ".join(self.cadd_object)))

    @staticmethod
    def _duplicate_chr_pos_ref_alt(dataset):
        dataset['chr_pos_ref_alt'] = dataset[['#Chrom', 'Pos', 'Ref', 'Alt']].astype(str).agg('_'.join, axis=1)
        return dataset

    def _process_objects(self, dataset: pd.DataFrame):
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
        self.log.info('Using features saved within the model.')
        return self.model._Booster.feature_names

    def _process_categorical_vars(self,
                                  dataset: pd.DataFrame,
                                  cadd_feats_names_dict,
                                  cadd_feats_levels_dict):
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
        return self.model_features

    # Model stuff

    @staticmethod
    @abstractmethod
    def get_supported_cadd_version():
        """
        Template for the model setup to tell CAPICE
        what CADD version is supported.
        :return: float
        """
        pass

    @staticmethod
    @abstractmethod
    def get_supported_genomebuild_version():
        """
        Template for the model setup to tell CAPICE what genome build is
        supported.
        :return: int
        """
        pass

    def predict(self, data: pd.DataFrame):
        """
        Template method for a model setup to predict and return scores.
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
