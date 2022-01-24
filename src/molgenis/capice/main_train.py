import json

import pandas as pd
import xgboost as xgb
from scipy import stats
from sklearn.model_selection import train_test_split, RandomizedSearchCV

from molgenis.capice.main_capice import Main
from molgenis.capice.__version__ import __version__
from molgenis.capice.utilities.enums import TrainEnums
from molgenis.capice.core.capice_exporter import CapiceExporter


class CapiceTrain(Main):
    """
    Train class of CAPICE to create new CAPICE like models for new or specific
    use cases.
    """

    def __init__(self, input_path, json_path, test_split, output_path):
        super().__init__(input_path, output_path)

        # Impute JSON.
        self.json_path = json_path
        self.log.debug('Input impute JSON confirmed: %s', self.json_path)

        # Train test size.
        self.train_test_size = test_split
        self.log.debug(
            'The percentage of data used for the testing dataset within training: %s',
            self.train_test_size)

        # Required features when file is loaded
        self.additional_required = ['binarized_label', 'sample_weight']
        self.exclude_features += self.additional_required

        # Variables that can be edited in testing to speed up the train testing
        self.esr = 15
        self.n_jobs = 8
        self.cross_validate = 5
        self.n_iterations = 20

        # (Other) global variables
        self.random_state = 45
        self.split_random_state = 4
        self.model_random_state = 0
        self.processed_features = []
        self.loglevel = self.manager.loglevel
        self.exporter = CapiceExporter(file_path=self.output)

    def run(self):
        """
        Main function. Will make a variety of calls to the required modules in
        order to create new CAPICE models.
        """
        data = self._load_file(additional_required_features=self.additional_required)
        data = self.process(loaded_data=data)
        with open(self.json_path, 'rt') as impute_values_file:
            json_dict = json.load(impute_values_file)
        self._validate_impute_complete(data, json_dict)

        imputed_data = self.impute(loaded_data=data, impute_values=json_dict)
        processed_data = self.preprocess(loaded_data=imputed_data)
        self._get_processed_features(dataset=processed_data, impute_keys=json_dict.keys())
        processed_train, processed_test = self.split_data(dataset=processed_data,
                                                          test_size=self.train_test_size)
        model = self.train(test_set=processed_test, train_set=processed_train)
        setattr(model, "impute_values", json_dict)
        setattr(model, 'CAPICE_version', __version__)
        self.exporter.export_capice_model(model=model)

    def _validate_impute_complete(self, dataset, json_dict):
        """

        :param pd.DataFrame dataset:
        :param dict json_dict:
        :return:
        """
        missing = []
        for key in json_dict.keys():
            if key not in dataset.columns:
                missing.append(key)

        if len(missing) > 0:
            error_message = 'Impute file missing needed columns for input file: %s'
            self.log.critical(error_message, missing)
            raise ValueError(error_message % missing)

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

    def _get_processed_features(self, dataset: pd.DataFrame, impute_keys):
        """
        Function to save the columns of a dataset that have been processed and
        thus are an output column of the CADD annotation.
        :param dataset: pandas.DataFrame
        """
        for column in dataset.columns:
            for feature in impute_keys:
                if (column == feature or column.startswith(feature)) and \
                        column not in self.processed_features:
                    self.processed_features.append(column)

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

        verbosity = 0
        xgb_verbosity = False

        # First checking if it is not None
        if self.loglevel and self.loglevel < 20:
            verbosity = 1
            xgb_verbosity = True

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
            random_state=self.model_random_state,
            use_label_encoder=False
        )
        ransearch1 = RandomizedSearchCV(estimator=model_estimator,
                                        param_distributions=param_dist,
                                        scoring='roc_auc', n_jobs=8,
                                        cv=self.cross_validate,
                                        n_iter=self.n_iterations,
                                        verbose=verbosity)

        if int(xgb.__version__.split('.')[0]) > 0:
            eval_set = [(test_set[self.processed_features],
                         test_set[TrainEnums.binarized_label.value])]
        else:
            eval_set = [(test_set[self.processed_features],
                         test_set[TrainEnums.binarized_label.value],
                         'test')]
        self.log.info('Random search starting, please hold.')
        ransearch1.fit(train_set[self.processed_features],
                       train_set[TrainEnums.binarized_label.value],
                       early_stopping_rounds=self.esr,
                       eval_metric=["auc"],
                       eval_set=eval_set,
                       verbose=xgb_verbosity,
                       sample_weight=train_set[TrainEnums.sample_weight.value])
        self.log.info(
            'Training successful, '
            'average CV AUC of best performing model: %.4f',
            ransearch1.best_score_)

        return ransearch1.best_estimator_
