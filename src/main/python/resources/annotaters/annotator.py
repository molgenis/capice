from src.main.python.core.logger import Logger
from src.main.python.core.global_manager import CapiceManager
from src.main.python.resources.annotaters.processer import ProcessorAnnotator
from src.main.python.resources.annotaters.lookup import LookupAnnotator
import pandas as pd


class Annotator:
    def __init__(self):
        self.log = Logger().logger
        self.manager = CapiceManager()

    def annotate(self, dataset: pd.DataFrame):
        """
        Start the annotation process.
        :param dataset: pandas dataframe
        :return: pandas dataframe similar to the output of the CADD pipeline
        """
        self.log.info('Starting annotation processing')
        annotated_dataset = dataset  # change once everything is ready
        return annotated_dataset

    @staticmethod
    def _correct_percentage_sign(dataset: pd.DataFrame):
        new_columns = []
        for column in dataset.columns:
            new_columns.append(column.split('%')[1])
        dataset.columns = new_columns
        return dataset
