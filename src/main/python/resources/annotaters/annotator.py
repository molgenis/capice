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
        self.dataset = dataset

    def annotate(self):
        """
        Start the annotation process.
        :return: pandas dataframe similar to the output of the CADD pipeline
        """
        self.log.info('Starting annotation processing')
        annotated_dataset = self.dataset  # change once everything is ready
        return annotated_dataset

    def _correct_percentage_sign(self):
        new_columns = []
        for column in self.dataset.columns:
            new_columns.append(column.split('%')[1])
        self.dataset.columns = new_columns

    def _add_sequence(self, dataset: pd.DataFrame):
        self.log.debug('Annotation addition: sequence')
        self.dataset['SEQ'] = dataset.apply(
            lambda x: self.fasta_lookup.get_reference_sequence(
                chromosome=x['CHROM'],
                start=x['POS'] - 75,
                end=x['POS'] + 75
            ), axis=1
        )
        self.fasta_lookup.close_connection()
