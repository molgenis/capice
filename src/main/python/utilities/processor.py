import pandas as pd
from src.main.python.core.logger import Logger
from src.main.python.core.global_manager import CapiceManager
from src.main.python.utilities.manual import ManualProcessor


class Processor:
    """
    Overseer class Processor to call the ManualProcessor and possibly future
    additions to processing.
    """
    def __init__(self, dataset: pd.DataFrame):
        """
        :param dataset: pandas.DataFrame, the loaded user provided input TSV of
        VEP-like origin.
        """
        self.log = Logger().logger
        self.manager = CapiceManager()
        self.manual_annotater = ManualProcessor()
        self.dataset = dataset

    def process(self):
        """
        Start the VEP output features processing.
        :return: pandas dataframe
        """
        self.log.info('Starting VEP features processing.')
        self.dataset = self.manual_annotater.process(dataset=self.dataset)
        self.log.info('Processing successful.')
        self.log.debug(
            'Final shape of the data: %s', self.dataset.shape)
        return self.dataset
