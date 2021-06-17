from src.main.python.core.logger import Logger
from src.main.python.core.global_manager import CapiceManager
from src.main.python.resources.annotaters.processer import ProcessorAnnotator
from src.main.python.resources.annotaters.lookup import LookupAnnotator, FastaLookupAnnotator
import pandas as pd


class Annotator:
    def __init__(self, dataset: pd.DataFrame):
        self.log = Logger().logger
        self.manager = CapiceManager()
        self.fasta_lookup = FastaLookupAnnotator()
        self.lookup = LookupAnnotator()
        self.manual_annotater = ProcessorAnnotator()
        self.dataset = dataset
        self._correct_percentage_sign()

    def annotate(self):
        """
        Start the annotation process.
        :return: pandas dataframe similar to the output of the CADD pipeline
        """
        self.log.info('Starting annotation process for {} samples (amount of columns: {})'.format(
            self.dataset.shape[0],
            self.dataset.shape[1]
        ))
        self._add_sequence()
        self.dataset = self.manual_annotater.process(dataset=self.dataset)
        self.log.info('Annotation for {} samples succesfull, amount of columns: {}'.format(self.dataset.shape[0],
                                                                                           self.dataset.shape[1]))
        return self.dataset

    def _correct_percentage_sign(self):
        new_columns = []
        for column in self.dataset.columns:
            new_columns.append(column.split('%')[1])
        self.dataset.columns = new_columns

    def _add_sequence(self):
        self.log.debug('Annotation addition: sequence')
        self.dataset['Seq'] = self.dataset.apply(
            lambda x: self.fasta_lookup.get_reference_sequence(
                chromosome=x['CHROM'],
                start=x['POS'] - 75,
                end=x['POS'] + 75
            ), axis=1
        )
        self.fasta_lookup.close_connection()
