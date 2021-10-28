import pandas as pd
import xgboost as xgb
from scipy import stats

from src.main.python.resources.__version__ import __version__
from src.main.python.resources.utilities.utilities import load_json_as_dict
from src.main_capice import Main
from src.main.python.core.exporter import Exporter
from src.main.python.resources.enums.sections import Train as EnumsTrain
from sklearn.model_selection import train_test_split, RandomizedSearchCV


class Train(Main):
    """
    Train class of CAPICE to create new CAPICE like models for new or specific
    use cases.
    """
    INPUT_ADDITIONAL_REQUIRED = ('binarized_label', 'sample_weight')
    IMPUTE_SKIP_LIST = INPUT_ADDITIONAL_REQUIRED + (
        'chr', 'pos', 'gene_name', 'gene_id', 'id_source', 'transcript')

    def __init__(self,
                 input_loc,
                 json_loc,
                 test_split,
                 output_loc):
        super().__init__(input_loc, output_loc)

        # Impute JSON.
        self.json_loc = json_loc
        self.log.debug(
            'Input impute JSON confirmed: %s', self.json_loc
        )

        # Train test size.
        self.train_test_size = test_split
        self.log.debug(
            'The percentage of data used for the testing dataset within '
            'training: %s', self.train_test_size
        )

        # (Other) global variables
        self.random_state = 45
        self.split_random_state = 4
        self.model_random_state = 0
        self.annotation_features = []
        self.processed_features = []
        self.loglevel = self.manager.loglevel
        self.model_type = None
        self.exporter = Exporter(file_path=self.output)
        self._integration_test = False  # Class should not have this knowledge!

    def run(self):
        """
        Main function. Will make a variety of calls to the required modules in
        order to create new CAPICE models.
        """
        data = self._load_file(
            additional_required_features=self.INPUT_ADDITIONAL_REQUIRED
        )
        data = self.process(loaded_data=data)
        json_dict = load_json_as_dict(self.json_loc)
        self._validate_impute_complete(data, json_dict, self.IMPUTE_SKIP_LIST)

        imputed_data = self.impute(loaded_data=data,
                                   impute_values=json_dict)
        processed_data = self.preprocess(loaded_data=imputed_data)
        self._get_processed_features(dataset=processed_data,
                                     impute_keys=json_dict.keys())
        processed_train, processed_test = self.split_data(
            dataset=processed_data,
            test_size=self.train_test_size
        )
        model = self.train(test_set=processed_test, train_set=processed_train)
        setattr(model, "impute_values", json_dict)
        setattr(model, 'CAPICE_version', __version__)
        self.exporter.export_capice_model(
            model=model, model_type=self.model_type
        )

    @staticmethod
    def _validate_impute_complete(dataset, json_dict, impute_skip_list):
        """

        :param pd.DataFrame dataset:
        :param dict json_dict:
        :param array impute_skip_list:
        :return:
        """
        missing = []
        for column in dataset.columns:
            if column not in impute_skip_list and column not in json_dict:
                missing.append(column)

        if len(missing) > 0:
            raise ValueError(f'Impute file missing needed columns for input '
                             f'file: {missing}')

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
        vars_in_range = variants[
            (variants[EnumsTrain.max_AF.value] >= lower) &
            (variants[EnumsTrain.max_AF.value] < upper)
            ].dropna(how='all')
        return vars_in_range

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
        if self.loglevel:
            if self.loglevel < 20:
                verbosity = 1
                xgb_verbosity = True

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
                test_set[EnumsTrain.binarized_label.value]
            )]
        else:
            eval_set = [(
                test_set[self.processed_features],
                test_set[EnumsTrain.binarized_label.value],
                'test'
            )]
        self.log.info('Random search starting, please hold.')
        ransearch1.fit(train_set[self.processed_features],
                       train_set[EnumsTrain.binarized_label.value],
                       early_stopping_rounds=early_stopping_rounds,
                       eval_metric=["auc"],
                       eval_set=eval_set,
                       verbose=xgb_verbosity,
                       sample_weight=train_set[EnumsTrain.sample_weight.value])

        return ransearch1
