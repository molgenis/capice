from src.main.python.core.logger import Logger
from src.main.python.core.global_manager import CapiceManager
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
