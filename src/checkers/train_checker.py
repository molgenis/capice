from src.logger import Logger
import pandas as pd


class TrainChecker:
    def __init__(self):
        self.log = Logger().get_logger()

    def specified_defaults_checker(self, loaded_defaults: dict):
        required_arguments = {'learning_rate': float, 'n_estimators': int, 'max_depth': int}
        for argument in required_arguments.keys():
            if argument not in loaded_defaults.keys():
                error_message = 'Argument {} is not found in the specified defaults file!'.format(argument)
                self.log.critical(error_message)
                raise KeyError(error_message)
            if not isinstance(loaded_defaults[argument], required_arguments[argument]):
                error_message = 'For argument expected type: {}, but got: {}'.format(
                    required_arguments[argument],
                    type(loaded_defaults[argument])
                )
                self.log.critical(error_message)
                raise TypeError(error_message)

    def check_labels(self, dataset: pd.DataFrame):
        required_columns = ['binarized_label', 'sample_weight']
        for col_name in required_columns:
            if col_name not in dataset.columns:
                error_message = 'Label {} not found within dataset! Please add it to your dataset.'.format(col_name)
                self.log.critical(error_message)
                raise KeyError(error_message)
