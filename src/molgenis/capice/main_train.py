import json

import numpy as np
import pandas as pd
import xgboost as xgb
from scipy import stats
from sklearn.model_selection import train_test_split, RandomizedSearchCV

from molgenis.capice.main_capice import Main
from molgenis.capice import __version__
from molgenis.capice.utilities import check_if_in_list
from molgenis.capice.utilities.enums import TrainEnums
from molgenis.capice.core.capice_exporter import CapiceExporter


class CapiceTrain(Main):
    """
    Train class of CAPICE to create new CAPICE like models for new or specific
    use cases.
    """

    def __init__(self, input_path, json_path, test_split, output_path, output_given, threads):
        super().__init__(input_path, output_path, output_given)

        # Impute JSON.
        self.json_path = json_path
        self.log.debug('Input model features JSON confirmed: %s', self.json_path)

        # Train test size.
        self.train_test_size = test_split
        self.log.debug(
            'The percentage of data used for the testing dataset within training: %s',
            self.train_test_size)

        # Required features when file is loaded
        self.additional_required = [TrainEnums.binarized_label.value,
                                    TrainEnums.sample_weight.value]
        self.exclude_features += self.additional_required

        # Variables that can be edited in testing to speed up the train testing
        self.esr = 15
        self.n_jobs = threads
        self.cross_validate = 5
        self.n_iterations = 20

        # (Other) global variables
        self.random_state = 45
        self.split_random_state = 4
        self.model_random_state = 0
        self.train_features = []
        self.loglevel = self.manager.loglevel
        self.exporter = CapiceExporter(file_path=self.output, output_given=self.output_given)

    def run(self):
        """
        Main function. Will make a variety of calls to the required modules in
        order to create new CAPICE models.
        """
        data = self._load_file(additional_required_features=self.additional_required)
        with open(self.json_path, 'rt') as impute_values_file:
            train_features = list(json.load(impute_values_file).keys())

        self._validate_train_features_duplicates(train_features)

        self._validate_features_present(data, train_features)

        data, vep_processed = self.process(
            loaded_data=data,
            process_features=train_features
        )

        processable_features = self._reset_processing_features(
            train_features,
            vep_processed,
            data.columns
        )

        processed_data, processed_features = self.categorical_process(
            loaded_data=data,
            train_features=processable_features,
            processing_features=None
        )

        self._set_train_features(processable_features, processed_features)

        processed_train, processed_test = self.split_data(dataset=processed_data,
                                                          test_size=self.train_test_size)
        model = self.train(test_set=processed_test, train_set=processed_train)
        setattr(model, "vep_features", vep_processed)
        setattr(model, "processable_features", processed_features)
        setattr(model, 'CAPICE_version', __version__)
        self.exporter.export_capice_model(model=model)

    def _validate_features_present(self, dataset, train_features) -> None:
        missing = []
        for key in train_features:
            if key not in dataset.columns:
                missing.append(key)

        if len(missing) > 0:
            error_message = 'Train features file missing needed columns for input file: %s'
            self.log.critical(error_message, missing)
            raise ValueError(error_message % missing)

    def _validate_train_features_duplicates(self, input_train_features: list):
        values, counts = np.unique(input_train_features, return_counts=True)
        if counts[counts > 1].any():
            error_message = 'Detected duplicate features in user supplied train features: %s'
            duplicates = ', '.join(values[counts > 1])
            self.log.critical(error_message, duplicates)
            raise KeyError(error_message % duplicates)

    @staticmethod
    def _reset_processing_features(
            input_train_features: list,
            vep_processed: dict,
            vep_processed_dataframe_columns: pd.DataFrame.columns
    ) -> list[str]:
        feature_list = []
        # Adds the VEP input features to which the processor has property drop = False
        for feature in vep_processed.keys():
            if feature in vep_processed_dataframe_columns:
                feature_list.append(feature)
        # Adds back the user input features, but avoiding adding duplicates and
        # avoiding the features that had property drop = True
        for feature in input_train_features:
            if feature not in feature_list and feature not in vep_processed.keys():
                feature_list.append(feature)
        # Extending the features with the VEP processors output features
        # Has to be new list otherwise features from feature_list go missing
        return_list = check_if_in_list(vep_processed.values(), feature_list)
        # Merging back with feature_list
        return_list.extend(feature_list)
        return return_list

    def _set_train_features(self, processable_features: list, processed_features: dict) -> \
            None:
        train_features = []
        for feature in processable_features:
            if feature not in processed_features.keys():
                train_features.append(feature)
        for feature_name, features in processed_features.items():
            for feature in features:
                train_features.append(f'{feature_name}_{feature}')
        self.log.info(
            'The following features have been selected for training: %s',
            ', '.join(train_features)
        )
        self.train_features = train_features

    def split_data(self, dataset, test_size: float):
        """
        Function to split any given dataset into 2 datasets using the test_size
        argument. Can export both if export flag is enabled.
        :param dataset: pandas.DataFrame
        :param test_size: float, ranging 0-1
        :return: train, test (1-test_size, test_size)
        """
        train, test = train_test_split(dataset,
                                       test_size=test_size,
                                       random_state=self.split_random_state)
        return train, test

    def _set_verbosity_from_log_level(self):
        """
        Uses loglevel to set verbosity and xg boost verbosity
        :return: tuple of int and bool
        verbosity, xgboost verbosity
        """
        verbosity = 0
        xgb_verbosity = False

        # First checking if it is not None
        if self.loglevel and self.loglevel < 20:
            verbosity = 1
            xgb_verbosity = True
        return verbosity, xgb_verbosity

    def _create_eval_set(self, xgb_version, test_set):
        """
        Creates the eval_set for xgb version, test set and processed features (0.x.x will be test).
        :param xgb_version: string
            xg boost version
        :param test_set: pandas DataFrame
            the testing dataset for determine performance during training
        :return: a list with tuple with pandas Dataframe, pandas Series and possibly "test"
        eval_set
        """
        eval_data = [test_set[self.train_features],
                     test_set[TrainEnums.binarized_label.value]]
        if int(xgb_version.split('.')[0]) < 1:
            eval_data.append('test')
        return [tuple(eval_data)]

    def train(self, test_set: pd.DataFrame, train_set: pd.DataFrame):
        """
        The training part of main_train.py after all has been processed.
        This is the same as Li et al. originally used to create CAPICE,
        but might be altered due to deprecation of certain libraries.
        :param test_set: pandas.DataFrame,
            the testing dataset for determine performance during training
        :param train_set: pandas.DataFrame,
            the training dataset on which the model will be created on
        """
        param_dist = {
            'max_depth': stats.randint(1, 20),
            # (random integer from 1 to 20)
            'learning_rate': stats.expon(scale=0.06),
            # (random double from an exponential with scale 0.06)
            'n_estimators': stats.randint(100, 600),
            # (random integer from 10 to 600)
        }

        verbosity, xgb_verbosity = self._set_verbosity_from_log_level()

        self.log.debug('Preparing the estimator model.')

        model_estimator = xgb.XGBClassifier(
            verbosity=verbosity,
            objective='binary:logistic',
            booster='gbtree', n_jobs=self.n_jobs,
            min_child_weight=1,
            max_delta_step=0,
            subsample=1, colsample_bytree=1,
            colsample_bylevel=1,
            colsample_bynode=1,
            reg_alpha=0, reg_lambda=1,
            scale_pos_weight=1,
            base_score=0.5,
            random_state=self.model_random_state
        )
        model_estimator.set_params(
            **{
                'eval_metric': ["auc"],
                'early_stopping_rounds': self.esr
            }
        )
        randomised_search_cv = RandomizedSearchCV(estimator=model_estimator,
                                                  param_distributions=param_dist,
                                                  scoring='roc_auc', n_jobs=8,
                                                  cv=self.cross_validate,
                                                  n_iter=self.n_iterations,
                                                  verbose=verbosity)

        eval_set = self._create_eval_set(xgb.__version__, test_set)

        self.log.info('Random search starting, please hold.')
        randomised_search_cv.fit(train_set[self.train_features],
                                 train_set[TrainEnums.binarized_label.value],
                                 eval_set=eval_set,
                                 verbose=xgb_verbosity,
                                 sample_weight=train_set[TrainEnums.sample_weight.value])
        self.log.info(
            'Training successful, '
            'average CV AUC of best performing model: %.4f',
            randomised_search_cv.best_score_
        )

        self.log.info(
            'Using parameters: %s',
            ', '.join([
                key + ': ' + str(value) for key, value in randomised_search_cv.best_params_.items()
            ])
        )

        return randomised_search_cv.best_estimator_
