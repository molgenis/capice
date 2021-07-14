from src.main.python.core.logger import Logger
import pandas as pd


class TrainChecker:
    """
    Class specific to the train_model.py to check certain parts within it's process.
    """
    def __init__(self):
        self.log = Logger().logger

    def check_specified_defaults(self, loaded_defaults: dict):
        """
        Function to check if "learning_rate", "n_estimators" and "max_depth" are present within the specified defaults
        file. Also check if the variable type of the parameters match the expected type.
        :param loaded_defaults: dict
        """
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

    def check_labels(self, dataset: pd.DataFrame, include_balancing=False):
        """
        Function to check if "binarized_label" and "sample_weight" are present within the columns of a given dataset.
        Set include_balancing to true if user wants to perform balancing algorithm.
        :param dataset: pandas DataFrame
        :param include_balancing: bool
        """
        required_columns = ['binarized_label', 'sample_weight']
        if include_balancing:
            required_columns += ['Consequence', 'MAX_AF']
        for col_name in required_columns:
            if col_name not in dataset.columns:
                error_message = 'Error locating label {} within dataset!'.format(col_name)
                self.log.critical(error_message)
                raise KeyError(error_message)
