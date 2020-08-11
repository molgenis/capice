#!/usr/bin/env python3

from src.preprocess import PreProcess
from src.utilities.utilities import prepare_dir
import pandas as pd
import numpy as np
import xgboost as xgb
import scipy
import pickle
import argparse
import os
from sklearn.model_selection import train_test_split, RandomizedSearchCV


class Train:
    def __init__(self, data_loc, output_loc, verbose, default,
                 balanced_set):
        self.verbose = verbose
        self._printf("Input location: {}".format(data_loc), flush=True)
        self.data_loc = data_loc
        self._printf("Output location: {}".format(output_loc), flush=True)
        self.output_loc = output_loc
        prepare_dir(self.output_loc)
        self._printf("Default set to: {}".format(str(default)),
                     flush=True)
        self.default = default
        self._printf("Balanced DS location: {}".format(balanced_set),
                     flush=True)
        self.balanced_set_input = balanced_set
        self.data = self._load_data()
        self.train_set = None
        self.test_set = None
        self.processed_features = []
        self.ransearch_output = os.path.join(self.output_loc,
                                             'xgb_ransearch.pickle.dat')
        self.optimal_model = os.path.join(self.output_loc,
                                          'xgb_optimal_model.pickle.dat')
        self.ip = PreProcess()
        self.cadd_vars = self.ip.get_cadd_vars()

        self._prepare_data()

    def _prepare_data(self):
        train, test = train_test_split(self.data, test_size=0.2, random_state=4)
        self.train_set = self.ip.preprocess(self.ip.impute(train), isTrain=True)
        for col in self.train_set.columns:
            for feat in self.cadd_vars:
                if col == feat or col.startswith(feat):
                    if col not in self.processed_features:
                        self.processed_features.append(col)
        self.test_set = self.ip.preprocess(
            self.ip.impute(test), isTrain=False,
            model_features=self.processed_features)

    def _load_data(self):
        if self.balanced_set_input:
            data = pd.read_csv(self.balanced_set_input,
                               sep='\t',
                               low_memory=False,
                               verbose=self.verbose)
            self._printf("Data loaded with shape: ", data.shape)
            return data
        else:
            data_to_be_balanced = pd.read_csv(self.data_loc,
                                              sep='\t',
                                              low_memory=False,
                                              verbose=self.verbose)
            self._printf("Data loaded with shape: ", data_to_be_balanced.shape)
            data = self._process_balance_in_the_force(data_to_be_balanced)
            self._export_balanced(data)
            return data

    def _export_balanced(self, balanced_ds):
        output_name = os.path.join(self.output_loc,
                                   'train_balanced_dataset.tsv.gz')
        balanced_ds.to_csv(output_name,
                           sep='\t',
                           compression='gzip',
                           index=False)
        self._printf("Exported balanced ds: \n{}\n(Shape={})".format(
            output_name, balanced_ds.shape), flush=True)

    def _process_balance_in_the_force(self, dataset: pd.DataFrame):
        palpatine = dataset[dataset['binarized_label'] == 1]
        yoda = dataset[dataset['binarized_label'] == 0]
        anakin = pd.DataFrame(columns=dataset.columns)
        # bins = [0, 0.1, 1]
        bins = [0, 0.01, 0.05, 0.1, 0.5, 1]
        for consequence in palpatine['Consequence'].unique():
            self._printf("Processsing: {}".format(consequence), flush=True)
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
                self._printf(
                    "Sampled {} variants from Possibly Neutral Variants for:"
                    " {} (in range of: {} - {})".format(
                        selected_pnv_currange.shape[0],
                        consequence,
                        lower_bound,
                        upper_bound),
                    flush=True
                )
                self._printf(
                    "Sampled {} variants from Possibly Pathogenic Variants for:"
                    " {} (in range of: {} - {})".format(
                        selected_pathogenic_currange.shape[0],
                        consequence,
                        lower_bound,
                        upper_bound),
                    flush=True
                )
                anakin = anakin.append(
                    selected_pnv_currange
                )
                anakin = anakin.append(
                    selected_pathogenic_currange
                )
        return anakin

    @staticmethod
    def _get_vars_in_range(variants, upper, lower):
        vars_in_range = variants.where(
            (variants['max_AF'] < upper) &
            (variants['max_AF'] >= lower)
        ).dropna(how='all')
        return vars_in_range

    def train(self):
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
        self._printf('Preparing the estimator model', flush=True)
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
        eval_set = [(self.test_set[self.processed_features],
                     self.test_set['binarized_label'], 'test')]
        self._printf('Random search initializing', flush=True)

        self._printf('Random search starting, please hold.', flush=True)
        ransearch1.fit(self.train_set[self.processed_features],
                       self.train_set['binarized_label'],
                       early_stopping_rounds=15,
                       eval_metric=["auc"],
                       eval_set=eval_set,
                       verbose=True,
                       sample_weight=self.train_set['sample_weight'])
        pickle.dump(ransearch1, open(self.ransearch_output, "wb"))

        if not self.default:
            pickle.dump(ransearch1.best_estimator_, open(self.optimal_model,
                                                         'wb'))

    def _printf(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)


class ArgumentSupporter:
    def __init__(self):
        parser = self._create_argument_parser()
        self.arguments = parser.parse_args()

    @staticmethod
    def _create_argument_parser():
        parser = argparse.ArgumentParser(
            prog="train_model.py",
            description="Python script to train new models using XGboost.")
        required = parser.add_argument_group("Required arguments")
        optional = parser.add_argument_group("Optional arguments")

        optional.add_argument('-f',
                              '--file',
                              nargs=1,
                              type=str,
                              default=None,
                              help='The location of the TSV training file. '
                                   'Will be made balanced, '
                                   'this balanced dataset will '
                                   'be output to -o. '
                                   'Will cause bias if training '
                                   'file contains indexing numbers.')

        optional.add_argument('-b',
                              '--balanced_ds',
                              nargs=1,
                              type=str,
                              default=None,
                              help='Use this argument if you already have a '
                                   'balanced dataset or dont\'t want to use '
                                   'a balanced dataset.')

        required.add_argument('-o',
                              '--output',
                              nargs=1,
                              type=str,
                              required=True,
                              help='The output directory to put the models in.')

        optional.add_argument('-d',
                              '--default',
                              action='store_true',
                              help='Use the python3.6 model hyperparameters.')

        optional.add_argument('-v',
                              '--verbose',
                              action='store_true',
                              help='Prints messages if called.')

        return parser

    def get_argument(self, argument_key):
        """
        Method to get a command line argument.
        :param argument_key: Command line argument.
        :return: List or string.
        """
        if self.arguments is not None and argument_key in self.arguments:
            value = getattr(self.arguments, argument_key)
        else:
            value = None

        return value


def main():
    arguments = ArgumentSupporter()
    input_loc = arguments.get_argument('file')
    if isinstance(input_loc, list):
        input_loc = str(input_loc[0])
    output_loc = arguments.get_argument('output')
    if isinstance(output_loc, list):
        output_loc = str(output_loc[0])
    balanced = arguments.get_argument('balanced_ds')
    if isinstance(balanced, list):
        balanced = str(balanced[0])
    verbose = arguments.get_argument('verbose')
    default = arguments.get_argument('default')
    _check_input(input_loc, balanced)
    train = Train(data_loc=input_loc, output_loc=output_loc,
                  verbose=verbose, default=default,
                  balanced_set=balanced)
    train.train()


def _check_input(data_loc, balanced_loc):
    if data_loc is None and balanced_loc is None:
        raise InputError('Data location must be specified.')


class InputError(Exception):
    pass


if __name__ == '__main__':
    main()
