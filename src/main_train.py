from src.main_capice import Main
from src.main.python.resources.checkers.train_checker import TrainChecker
from src.main.python.resources.enums.sections import Train as enums_train
from src.main.python.core.exporter import Exporter
import pandas as pd
import numpy as np
import xgboost as xgb
import scipy
import json
from sklearn.model_selection import train_test_split, RandomizedSearchCV


class Train(Main):
    """
    Train class of CAPICE to create new CAPICE like models for new or specific
    use cases.
    """

    def __init__(self,
                 __program__,
                 __author__,
                 __version__,
                 input_loc,
                 output_loc):
        super().__init__(__program__=__program__,
                         __author__=__author__,
                         __version__=__version__,
                         input_loc=input_loc,
                         output_loc=output_loc)

        # Argument logging
        self.balance = self.config.get_train_value('makebalanced')
        self.log.debug(
            'Make input dataset balanced confirmed: {}'.format(self.balance)
        )
        self.default = self.config.get_train_value('default')
        self.log.debug(
            'The use of the default Python 3.6 hyperparameters set to: '
            '{}'.format(self.default)
        )
        self.specified_default = self.config.get_train_value(
            'specifieddefaults'
        )
        self.log.debug(
            'The use of specified default hyperparameters set to: '
            '{}'.format(self.specified_default)
        )
        self.n_split = self.config.get_train_value('split')
        self.log.debug(
            'Split has been confirmed, set to: {}'.format(self.n_split)
        )
        self.early_exit = self.config.get_train_value('earlyexit')
        if self.early_exit:
            self.log.debug('Early exit flag confirmed.')
        self.train_test_size = self.config.get_train_value('traintestsize')
        self.log.debug(
            'The percentage of data used for the '
            'testing dataset within training: {}'.format(
                self.train_test_size)
        )

        # Global variables
        self.random_state = 45
        self.split_random_state = 4
        self.model_random_state = 0
        self.defaults = {}
        self.annotation_features = []
        self.processed_features = []
        self.loglevel = self.manager.loglevel
        self.model_type = None
        self.exporter = Exporter(file_path=self.output)
        self._integration_test = False

    def run(self):
        """
        Main function. Will make a variety of calls to the required modules in
        order to create new CAPICE models.
        """
        data = self._rename_chrom_col(self.load_file())
        data = self.annotate(loaded_data=data)
        train_checker = TrainChecker()
        train_checker.check_labels(dataset=data, include_balancing=self.balance)
        if self.balance:
            data = self.process_balance_in_the_force(dataset=data)
        if self.n_split > 0.0:
            self.log.info(
                'Splitting input dataset before any preprocessing happens.'
            )
            data, _ = self.split_data(
                dataset=data, test_size=self.n_split,
                export=True
            )
        if self.balance:
            self.exporter.export_capice_training_dataset(
                datafile=data,
                feature='balanced dataset',
                name='balanced_dataset'
            )
        self.load_defaults()
        if self.early_exit:
            exit('Early exit command was called, exiting.')
        imputed_data = self.impute(loaded_data=data, train=True)
        self.annotation_features = self.manager.annotation_features
        processed_data = self.preprocess(
            loaded_data=imputed_data, train=True
        )[1]
        self._get_processed_features(dataset=processed_data)
        processed_train, processed_test = self.split_data(
            dataset=processed_data,
            test_size=self.train_test_size
        )
        model = self.train(test_set=processed_test, train_set=processed_train)
        self.exporter.export_capice_model(
            model=model, model_type=self.model_type
        )

    @staticmethod
    def _rename_chrom_col(dataset):
        dataset.rename(columns={'#Chrom': 'Chr'}, inplace=True)
        return dataset

    def split_data(self, dataset, test_size: float, export: bool = False):
        """
        Function to split any given dataset into 2 datasets using the test_size
        argument. Can export both if export flag is enabled.
        :param dataset: pandas.DataFrame
        :param test_size: float, ranging 0-1
        :param export: boolean
        :return: train, test (1-test_size, test_size)
        """
        train, test = train_test_split(
            dataset,
            test_size=test_size,
            random_state=self.split_random_state
        )
        if export:
            self.exporter.export_capice_training_dataset(
                datafile=train,
                name='splitted_train_dataset',
                feature='splitted train'
            )
            self.exporter.export_capice_training_dataset(
                datafile=test,
                name='splitted_test_dataset',
                feature='splitted test'
            )
        return train, test

    def load_defaults(self):
        """
        Function to load in specified default hyper parameters.
        If no specified default is supplied, but -d flag is used,
        load in the original hyper parameters.
        Note: in any case the original hyper parameters will be loaded,
        but due to the absence of the -d or -sd flag,
        the self.defaults will not be used.
        """
        if self.specified_default:
            train_checker = TrainChecker()
            with open(self.specified_default) as json_file:
                defaults = json.load(json_file)
            train_checker.check_specified_defaults(loaded_defaults=defaults)
            self.log.debug(
                'Specified defaults located at {} successfully loaded.'.format(
                    self.specified_default
                )
            )
            self.default = True
        else:
            defaults = {
                enums_train.learning_rate.value: 0.10495845238185281,
                enums_train.max_depth.value: 422,
                enums_train.n_estimators.value: 15
            }
        self.defaults = defaults

    def process_balance_in_the_force(self, dataset: pd.DataFrame):
        """
        Balancing function as first used by Li et al. in the original
        CAPICE paper. Balances baced on Consequence,
        allele frequency and benign/pathogenic samples.
        :param dataset: pandas.DataFrame
        :return: balanced pandas.DataFrame
        """
        self.log.info('Balancing out the input dataset, please hold.')
        palpatine = dataset[dataset[enums_train.binarized_label.value] == 1]
        yoda = dataset[dataset[enums_train.binarized_label.value] == 0]
        anakin = pd.DataFrame(columns=dataset.columns)
        bins = [0, 0.01, 0.05, 0.1, 0.5, 1]
        for consequence in palpatine[enums_train.Consequence.value].unique():
            processed_consequence = self._process_consequence(
                pathogenic_dataframe=palpatine,
                benign_dataframe=yoda,
                return_df_columns=anakin.columns,
                bins=bins,
                consequence=consequence
            )
            anakin = anakin.append(processed_consequence)
        self.log.info('Balancing complete.')
        return anakin

    def _process_consequence(self,
                             pathogenic_dataframe: pd.DataFrame,
                             benign_dataframe: pd.DataFrame,
                             return_df_columns: list,
                             consequence: str,
                             bins: list):
        self.log.debug("Processsing: {}".format(consequence))
        selected_pathogenic = pathogenic_dataframe[
            pathogenic_dataframe[enums_train.Consequence.value] == consequence]
        selected_neutral = benign_dataframe[
            benign_dataframe[enums_train.Consequence.value] == consequence
            ]
        if selected_pathogenic.shape[0] > selected_neutral.shape[0]:
            selected_pathogenic = selected_pathogenic.sample(
                selected_neutral.shape[0],
                random_state=self.random_state
            )
        selected_pathogenic_histogram, bins = np.histogram(
            selected_pathogenic[enums_train.max_AF.value],
            bins=bins
        )
        return_df = pd.DataFrame(columns=return_df_columns)
        for ind in range(len(bins) - 1):
            upper_bound = bins[ind]
            lower_bound = bins[ind + 1]
            sample_number = selected_pathogenic_histogram[ind]
            processed_bins = self._process_bins(
                selected_pathogenic=selected_pathogenic,
                selected_neutral=selected_neutral,
                upper_bound=upper_bound,
                lower_bound=lower_bound,
                sample_num=sample_number
            )
            return_df = return_df.append(processed_bins)
        return return_df

    def _process_bins(self,
                      selected_pathogenic: pd.DataFrame,
                      selected_neutral: pd.DataFrame,
                      upper_bound: int,
                      lower_bound: int,
                      sample_num: int):
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
        if sample_num < selected_pnv_all.shape[0]:
            selected_pnv_currange = selected_pnv_all.sample(
                sample_num,
                random_state=self.random_state
            )
            selected_pathogenic_currange = selected_pathogenic_all
        else:
            selected_pnv_currange = selected_pnv_all
            selected_pathogenic_currange = selected_pathogenic_all.sample(
                selected_pnv_all.shape[0],
                random_state=self.random_state
            )
        self.log.debug(
            "Sampled {} variants from Possibly Neutral Variants in range of: "
            "{} - {}".format(
                selected_pnv_currange.shape[0],
                lower_bound,
                upper_bound)
        )
        self.log.debug(
            "Sampled {} variants from Possibly Pathogenic Variants in range "
            "of: {} - {}".format(
                selected_pathogenic_currange.shape[0],
                lower_bound,
                upper_bound)
        )
        return selected_pathogenic_currange.append(selected_pnv_currange)

    @staticmethod
    def _get_vars_in_range(variants: pd.DataFrame, upper: float, lower: float):
        """
        Sub-function of the balancing function to get variants within a certain
        allele frequency threshold.
        :param variants: pandas.DataFrame
        :param upper: float
        :param lower: float
        :return: pandas.DataFrame
        """
        vars_in_range = variants.where(
            (variants[enums_train.max_AF.value] < upper) &
            (variants[enums_train.max_AF.value] >= lower)
        ).dropna(how='all')
        return vars_in_range

    def _get_processed_features(self, dataset: pd.DataFrame):
        """
        Function to save the columns of a dataset that have been processed and
        thus are an output column of the CADD annotation.
        :param dataset: pandas.DataFrame
        """
        for column in dataset.columns:
            for feature in self.annotation_features:
                if column == feature or column.startswith(feature):
                    if column not in self.processed_features:
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
            'max_depth': scipy.stats.randint(1, 20),
            # (random integer from 1 to 20)
            'learning_rate': scipy.stats.expon(scale=0.06),
            # (random double from an exponential with scale 0.06)
            'n_estimators': scipy.stats.randint(100, 600),
            # (random integer from 10 to 600)
        }

        # First checking if it is not None
        if self.loglevel:
            if self.loglevel < 20:
                verbosity = 1
                xgb_verbosity = True
        else:
            verbosity = 0
            xgb_verbosity = False
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
                random_state=self.model_random_state,
                learning_rate=self.defaults[enums_train.learning_rate.value],
                n_estimators=self.defaults[enums_train.n_estimators.value],
                max_depth=self.defaults[enums_train.max_depth.value]
            )
            ransearch1 = model_estimator
            self.model_type = 'XGBClassifier'
        else:
            model_estimator = xgb.XGBClassifier(
                verbosity=verbosity,
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
                random_state=self.model_random_state,
                use_label_encoder=False
            )
            ransearch1 = RandomizedSearchCV(estimator=model_estimator,
                                            param_distributions=param_dist,
                                            scoring='roc_auc', n_jobs=8,
                                            cv=cv,
                                            n_iter=n_iter,
                                            verbose=verbosity)
            self.model_type = 'RandomizedSearchCV'
        if int(xgb.__version__.split('.')[0]) > 0:
            eval_set = [(
                test_set[self.processed_features],
                test_set[enums_train.binarized_label.value]
            )]
        else:
            eval_set = [(
                test_set[self.processed_features],
                test_set[enums_train.binarized_label.value],
                'test'
            )]
        self.log.info('Random search starting, please hold.')
        ransearch1.fit(train_set[self.processed_features],
                       train_set[enums_train.binarized_label.value],
                       early_stopping_rounds=early_stopping_rounds,
                       eval_metric=["auc"],
                       eval_set=eval_set,
                       verbose=xgb_verbosity,
                       sample_weight=train_set[enums_train.sample_weight.value])

        return ransearch1
