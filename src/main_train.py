from src.main import Main
from src.logger import Logger
from src.global_manager import CapiceManager
from src.checkers.train_checker import TrainChecker
from src.exporter import Exporter
import pandas as pd
import numpy as np
import xgboost as xgb
import scipy
import json
from sklearn.model_selection import train_test_split, RandomizedSearchCV


class Train:
    """
    Train class of CAPICE to create new CAPICE like models for new or specific use cases.
    """
    def __init__(self,
                 __program__,
                 __author__,
                 __version__,
                 input_loc,
                 output_loc,
                 balance,
                 default,
                 specified_default,
                 split,
                 early_exit,
                 train_test_size):

        self.manager = CapiceManager()
        self.log = Logger().logger
        self.__program__ = __program__
        self.__author__ = __author__
        self.__version__ = __version__

        # Argument logging
        self.input_loc = input_loc
        self.output_loc = output_loc
        self.balance = balance
        self.log.debug('Make input dataset balanced confirmed: {}'.format(self.balance))
        self.default = default
        self.log.debug('The use of the default Python 3.6 hyperparameters set to: {}'.format(self.default))
        self.specified_default = specified_default
        self.log.debug('The use of specified default hyperparameters set to: {}'.format(self.specified_default))
        self.n_split = split
        self.log.debug('Split has been confirmed, set to: {}'.format(self.n_split))
        self.early_exit = early_exit
        if self.early_exit:
            self.log.debug('Early exit flag confirmed.')
        self.train_test_size = train_test_size
        self.log.debug('The percentage of data used for the testing dataset within training: {}'.format(
            self.train_test_size))
        self.defaults = {}
        self.cadd_features = []
        self.processed_features = []
        self.verbose = self.manager.verbose
        self.model_type = None
        self.exporter = Exporter(file_path=self.output_loc)
        self._integration_test = False

    def main(self):
        """
        Main function. Will make a variety of calls to the required modules in order to create new CAPICE models.
        """
        input_loc = self.input_loc
        capice_processing = Main(__program__=self.__program__,
                                 __author__=self.__author__,
                                 __version__=self.__version__,
                                 input_loc=input_loc,
                                 output_loc=self.output_loc,
                                 genome_build=None,
                                 cadd_build=None)
        data = capice_processing.load_file()
        train_checker = TrainChecker()
        train_checker.check_labels(dataset=data)
        if self.balance:
            train_checker.check_balancing_labels(dataset=data)
            data = self.process_balance_in_the_force(dataset=data)
        if self.n_split:
            self.log.info('Splitting input dataset before any preprocessing happens.')
            data, _ = self.split_data(dataset=data, test_size=self.n_split, export=True)
        if self.balance:
            self.exporter.export_capice_training_dataset(datafile=data,
                                                         feature='balanced dataset',
                                                         name='balanced_dataset')
        self.load_defaults()
        if self.early_exit:
            exit('Early exit command was called, exiting.')
        imputed_data = capice_processing.impute(loaded_cadd_data=data)
        self.cadd_features = self.manager.cadd_features
        processed_data = capice_processing.preprocess(loaded_cadd_data=imputed_data, train=True)[1]
        self._get_processed_features(dataset=processed_data)
        processed_train, processed_test = self.split_data(dataset=processed_data,
                                                          test_size=self.train_test_size)
        model = self.train(test_set=processed_test, train_set=processed_train)
        self.exporter.export_capice_model(model=model, model_type=self.model_type)

    def split_data(self, dataset, test_size: float, export: bool = False):
        """
        Function to split any given dataset into 2 datasets using the test_size argument. Can export both if export
        flag is enabled.
        :param dataset: pandas.DataFrame
        :param test_size: float, ranging 0-1
        :param export: boolean
        :return: train, test (1-test_size, test_size)
        """
        train, test = train_test_split(dataset, test_size=test_size, random_state=4)
        if export:
            self.exporter.export_capice_training_dataset(datafile=train,
                                                         name='splitted_train_dataset',
                                                         feature='splitted train')
            self.exporter.export_capice_training_dataset(datafile=test,
                                                         name='splitted_test_dataset',
                                                         feature='splitted test')
        return train, test

    def load_defaults(self):
        """
        Function to load in specified default hyper parameters. If no specified default is supplied, but -d flag is
        used, load in the original hyper parameters. Note: in any case the original hyper parameters will be loaded,
        but due to the absence of the -d or -sd flag, the self.defaults will not be used.
        """
        if self.specified_default:
            train_checker = TrainChecker()
            with open(self.specified_default) as json_file:
                defaults = json.load(json_file)
            train_checker.specified_defaults_checker(loaded_defaults=defaults)
            self.log.debug('Specified defaults located at {} successfully loaded.'.format(self.specified_default))
            self.default = True
        else:
            defaults = {
                'learning_rate': 0.10495845238185281,
                'max_depth': 422,
                'n_estimators': 15
            }
        self.defaults = defaults

    def process_balance_in_the_force(self, dataset: pd.DataFrame):
        """
        Balancing function as first used by Li et al. in the original CAPICE paper. Balances baced on Consequence,
        allele frequency and benign/pathogenic samples.
        :param dataset: pandas.DataFrame
        :return: balanced pandas.DataFrame
        """
        self.log.info('Balancing out the input dataset, please hold.')
        palpatine = dataset[dataset['binarized_label'] == 1]
        yoda = dataset[dataset['binarized_label'] == 0]
        anakin = pd.DataFrame(columns=dataset.columns)
        bins = [0, 0.01, 0.05, 0.1, 0.5, 1]
        for consequence in palpatine['Consequence'].unique():
            self.log.debug("Processsing: {}".format(consequence))
            selected_pathogenic = palpatine[
                palpatine['Consequence'] == consequence]
            selected_neutral = yoda[yoda['Consequence'] == consequence]
            if selected_pathogenic.shape[0] > selected_neutral.shape[0]:
                selected_pathogenic = selected_pathogenic.sample(
                    selected_neutral.shape[0],
                    random_state=45
                )
            selected_pathogenic_histogram, bins = np.histogram(
                selected_pathogenic['max_AF'],
                bins=bins
            )
            for ind in range(len(bins) - 1):
                lower_bound = bins[ind]
                upper_bound = bins[ind + 1]
                selected_pathogenic_all = self._get_vars_in_range(
                    variants=selected_pathogenic,
                    upper=upper_bound,
                    lower=lower_bound
                )
                selected_pnv_all = self._get_vars_in_range(
                    variants=selected_neutral,
                    upper=upper_bound,
                    lower=lower_bound
                )
                sample_num = selected_pathogenic_histogram[ind]
                if sample_num < selected_pnv_all.shape[0]:
                    selected_pnv_currange = selected_pnv_all.sample(
                        sample_num,
                        random_state=45
                    )
                    selected_pathogenic_currange = selected_pathogenic_all
                else:
                    selected_pnv_currange = selected_pnv_all
                    selected_pathogenic_currange = \
                        selected_pathogenic_all.sample(
                            selected_pnv_all.shape[0],
                            random_state=45
                        )
                self.log.debug(
                    "Sampled {} variants from Possibly Neutral Variants for:"
                    " {} (in range of: {} - {})".format(
                        selected_pnv_currange.shape[0],
                        consequence,
                        lower_bound,
                        upper_bound)
                )
                self.log.debug(
                    "Sampled {} variants from Possibly Pathogenic Variants for:"
                    " {} (in range of: {} - {})".format(
                        selected_pathogenic_currange.shape[0],
                        consequence,
                        lower_bound,
                        upper_bound)
                )
                anakin = anakin.append(
                    selected_pnv_currange
                )
                anakin = anakin.append(
                    selected_pathogenic_currange
                )
        self.log.info('Balancing complete.')
        return anakin

    @staticmethod
    def _get_vars_in_range(variants: pd.DataFrame, upper: float, lower: float):
        """
        Sub-function of the balancing function to get variants within a certain allele frequency threshold.
        :param variants: pandas.DataFrame
        :param upper: float
        :param lower: float
        :return: pandas.DataFrame
        """
        vars_in_range = variants.where(
            (variants['max_AF'] < upper) &
            (variants['max_AF'] >= lower)
        ).dropna(how='all')
        return vars_in_range

    def _get_processed_features(self, dataset: pd.DataFrame):
        """
        Function to save the columns of a dataset that have been processed and thus are an output column of the CADD
        annotation.
        :param dataset: pandas.DataFrame
        """
        for column in dataset.columns:
            for feature in self.cadd_features:
                if column == feature or column.startswith(feature):
                    if column not in self.processed_features:
                        self.processed_features.append(column)

    def train(self, test_set: pd.DataFrame, train_set: pd.DataFrame):
        """
        The training part of main_train.py after all has been processed. This is the same as Li et al. originally used
        to create CAPICE, but might be altered due to deprecation of certain libraries.
        :param test_set: pandas.DataFrame, the testing dataset for determine performance during training
        :param train_set: pandas.DataFrame, the training dataset on which the model will be created on
        """
        param_dist = {
            'max_depth': scipy.stats.randint(1, 20),
            # (random integer from 1 to 20)
            'learning_rate': scipy.stats.expon(scale=0.06),
            # (random double from an exponential with scale 0.06)
            'n_estimators': scipy.stats.randint(100, 600),
            # (random integer from 10 to 600)
        }
        if self.verbose:
            verbosity = 1
        else:
            verbosity = 0
        self.log.debug('Preparing the estimator model.')

        if self._integration_test:
            early_stopping_rounds = 1
            n_jobs = 2
            cv = 2
            n_iter = 2
        else:
            early_stopping_rounds = 15
            n_jobs = 8
            cv = 5
            n_iter = 20

        if self.default:
            model_estimator = xgb.XGBClassifier(
                verbosity=verbosity,
                objective='binary:logistic',
                booster='gbtree', n_jobs=n_jobs,
                min_child_weight=1,
                max_delta_step=0,
                subsample=1,
                colsample_bytree=1,
                colsample_bylevel=1,
                colsample_bynode=1,
                reg_alpha=0, reg_lambda=1,
                scale_pos_weight=1,
                base_score=0.5,
                random_state=0,
                learning_rate=self.defaults['learning_rate'],
                n_estimators=self.defaults['n_estimators'],
                max_depth=self.defaults['max_depth']
            )
            ransearch1 = model_estimator
            self.model_type = 'XGBClassifier'
        else:
            model_estimator = xgb.XGBClassifier(verbosity=verbosity,
                                                objective='binary:logistic',
                                                booster='gbtree', n_jobs=n_jobs,
                                                min_child_weight=1,
                                                max_delta_step=0,
                                                subsample=1, colsample_bytree=1,
                                                colsample_bylevel=1,
                                                colsample_bynode=1,
                                                reg_alpha=0, reg_lambda=1,
                                                scale_pos_weight=1,
                                                base_score=0.5,
                                                random_state=0)
            ransearch1 = RandomizedSearchCV(estimator=model_estimator,
                                            param_distributions=param_dist,
                                            scoring='roc_auc', n_jobs=8,
                                            cv=cv,
                                            n_iter=n_iter,
                                            verbose=verbosity)
            self.model_type = 'RandomizedSearchCV'
        eval_set = [(test_set[self.processed_features],
                     test_set['binarized_label'], 'test')]
        self.log.info('Random search starting, please hold.')
        ransearch1.fit(train_set[self.processed_features],
                       train_set['binarized_label'],
                       early_stopping_rounds=early_stopping_rounds,
                       eval_metric=["auc"],
                       eval_set=eval_set,
                       verbose=True,
                       sample_weight=train_set['sample_weight'])

        return ransearch1
