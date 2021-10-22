from src.main.python.core.logger import Logger
from src.main.python.core.global_manager import CapiceManager
from src.main.python.resources.processors.manual import ManualProcessor
from src.main.python.resources.processors.lookup import FastaLookupAnnotator
import pandas as pd


class Processor:
    def __init__(self, dataset: pd.DataFrame):
        self.log = Logger().logger
        self.manager = CapiceManager()
        self.fasta_lookup = FastaLookupAnnotator()
        self.manual_annotater = ManualProcessor()
        self.dataset = dataset

    def process(self):
        """
        Start the VEP output features processing.
        :return: pandas dataframe
        """
        self.log.info('Starting VEP features processing.')
        # self._add_sequence()
        self.dataset = self.manual_annotater.process(dataset=self.dataset)
        self.log.info('Processing successful.')
        self.log.debug(
            'Final shape of the data: %s', self.dataset.shape)
        return self.dataset

    def _add_sequence(self):
        self.log.debug('Annotation addition: sequence')
        self.dataset['Seq'] = self.dataset.apply(
            lambda x: self.fasta_lookup.get_reference_sequence(
                chromosome=x['Chr'],
                start=x['Pos'] - 75,
                end=x['Pos'] + 75
            ), axis=1
        )
        self.fasta_lookup.close_connection()
