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
    def __init__(self,
                 __program__,
                 __author__,
                 __version__,
                 input_loc,
                 output_loc,
                 balanced_loc,
                 default,
                 specified_default,
                 split,
                 early_exit,
                 train_test_size):

        self.manager = CapiceManager()
        self.log = Logger().get_logger()
        self.__program__ = __program__
        self.__author__ = __author__
        self.__version__ = __version__

        # Argument logging
        self.input_loc = input_loc
        self.output_loc = output_loc
        self.balanced_loc = balanced_loc
        self.log.debug('Balanced dataset location confirmed: {}'.format(self.balanced_loc))
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
        self.verbose = self.manager.get_verbose()
        self.model_type = None
        self.exporter = Exporter(file_path=self.output_loc)

    def main(self):
        if self.input_loc:
            input_loc = self.input_loc
            make_balanced = True
        else:
            input_loc = self.balanced_loc
            make_balanced = False
        capice_processing = Main(__program__=self.__program__,
                                 __author__=self.__author__,
                                 __version__=self.__version__,
                                 input_loc=input_loc,
                                 output_loc=self.output_loc,
                                 genome_build=None,
                                 cadd_build=None)
        data = capice_processing.load_file(check_version_present=False)
        train_checker = TrainChecker()
        train_checker.check_labels(dataset=data)
        if make_balanced:
            data = self._process_balance_in_the_force(dataset=data)
        if self.n_split:
            self.log.info('Splitting input dataset before any preprocessing happens.')
            data, _ = self._split_data(dataset=data, test_size=self.n_split)
        if make_balanced:
            self.exporter.export_capice_training_dataset(datafile=data,
                                                         feature='balanced dataset',
                                                         name='balanced_dataset')
        self._load_defaults()
        if self.early_exit:
            exit('Early exit command was called, exiting.')
        imputed_data = capice_processing.impute(loaded_cadd_data=data)
        self.cadd_features = self.manager.get_cadd_features()
        processed_data = capice_processing.preprocess(loaded_cadd_data=imputed_data, train=True)[1]
        self._get_processed_features(dataset=processed_data)
        processed_train, processed_test = self._split_data(dataset=processed_data,
                                                           test_size=self.train_test_size,
                                                           export=False)
        model = self._train(test_set=processed_test, train_set=processed_train)
        self.exporter.export_capice_model(model=model, model_type=self.model_type)

    def _split_data(self, dataset, test_size: float, export: bool = True):
        train, test = train_test_split(dataset, test_size=test_size, random_state=4)
        if export:
            self.exporter.export_capice_training_dataset(datafile=train,
                                                         name='splitted_train_dataset',
                                                         feature='splitted train')
            self.exporter.export_capice_training_dataset(datafile=test,
                                                         name='splitted_test_dataset',
                                                         feature='splitted test')

        return train, test

    def _load_defaults(self):
        if self.specified_default:
            train_checker = TrainChecker()
            with open(self.specified_default) as json_file:
                defaults = json.load(json_file)
            train_checker.specified_defaults_checker(loaded_defaults=defaults)
        else:
            defaults = {
                'learning_rate': 0.10495845238185281,
                'max_depth': 422,
                'n_estimators': 15
            }
        self.defaults = defaults

    def _process_balance_in_the_force(self, dataset: pd.DataFrame):
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
        vars_in_range = variants.where(
            (variants['max_AF'] < upper) &
            (variants['max_AF'] >= lower)
        ).dropna(how='all')
        return vars_in_range

    def _get_processed_features(self, dataset: pd.DataFrame):
        for column in dataset.columns:
            for feature in self.cadd_features:
                if column == feature or column.startswith(feature):
                    if column not in self.processed_features:
                        self.processed_features.append(column)

    def _train(self, test_set: pd.DataFrame, train_set: pd.DataFrame):
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
        if self.default:
            model_estimator = xgb.XGBClassifier(
                verbosity=verbosity,
                objective='binary:logistic',
                booster='gbtree', n_jobs=8,
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
                learning_rate=0.10495845238185281,
                n_estimators=422,
                max_depth=15
            )
            ransearch1 = model_estimator
            self.model_type = 'XGBClassifier'
        else:
            model_estimator = xgb.XGBClassifier(verbosity=verbosity,
                                                objective='binary:logistic',
                                                booster='gbtree', n_jobs=8,
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
                                            cv=5,
                                            n_iter=20,
                                            verbose=verbosity)
            self.model_type = 'RandomizedSearchCV'
        eval_set = [(test_set[self.processed_features],
                     test_set['binarized_label'], 'test')]
        self.log.info('Random search starting, please hold.')
        ransearch1.fit(train_set[self.processed_features],
                       train_set['binarized_label'],
                       early_stopping_rounds=15,
                       eval_metric=["auc"],
                       eval_set=eval_set,
                       verbose=True,
                       sample_weight=train_set['sample_weight'])

        return ransearch1
