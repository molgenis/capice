import pandas as pd

from molgenis.capice.utilities.enums import Column, OutputClasses


class ClassSuggestor:
    def __init__(self):
        # Implement way to make thresholds datafile user definable
        pass

    @staticmethod
    def apply_suggestion(capice_predicted_dataset: pd.DataFrame):
        """
        Method to apply the suggested output class to a capice prediction score
        keeping in mind the per gene thresholds.

        :param capice_predicted_dataset: pandas.DataFrame.
            The input dataset that contains the "score" column and a gene name column.
        :return: pandas.DataFrame.
            Original input but with the column suggested_class, depending on the user provided
            thresholds.
        """
        capice_predicted_dataset[Column.suggested_class.value] = OutputClasses.unknown.value
        return capice_predicted_dataset
