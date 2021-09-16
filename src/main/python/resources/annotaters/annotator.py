from src.main.python.core.logger import Logger
from src.main.python.core.global_manager import CapiceManager
from src.main.python.resources.annotaters.manual import ManualAnnotator
from src.main.python.resources.annotaters.lookup import FastaLookupAnnotator
import pandas as pd


class Annotator:
    def __init__(self, dataset: pd.DataFrame):
        self.log = Logger().logger
        self.manager = CapiceManager()
        self.fasta_lookup = FastaLookupAnnotator()
        self.manual_annotater = ManualAnnotator()
        self.dataset = dataset

    def annotate(self):
        """
        Start the annotation process.
        :return: pandas dataframe
        """
        self.log.info('Starting manual annotation process.')
        self._add_sequence()
        self.dataset = self.manual_annotater.process(dataset=self.dataset)
        self.log.info('Annotation successful.')
        self.log.debug(f'Final shape of the annotated data: {self.dataset.shape}')
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
