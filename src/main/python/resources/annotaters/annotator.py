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
        self.manual_annotater = ProcessorAnnotator()
        self.dataset = dataset
        self._correct_percentage_sign()
        self._col_renamer()
        self.lookup = LookupAnnotator()

    def annotate(self):
        """
        Start the annotation process.
        :return: pandas dataframe similar to the output of the CADD pipeline
        """
        self.log.info('Starting manual annotation process.')
        self._add_sequence()
        self.dataset = self.manual_annotater.process(dataset=self.dataset)
        self.log.info('Manual annotation successful.')
        self.log.info('Starting annotation using CADD database, please hold.')
        self.dataset = self.lookup.process(dataset=self.dataset)
        self.log.info('Annotation successful.')
        self.log.debug('Final shape of the annotated data: {}'.format(self.dataset.shape))
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
                chromosome=x['Chr'],
                start=x['Pos'] - 75,
                end=x['Pos'] + 75
            ), axis=1
        )
        self.fasta_lookup.close_connection()

    def _col_renamer(self):
        """
        Function to rename "Gene, Feature, SYMBOL, INTRON and EXON" to
        "GeneID, FeatureID, GeneName, Intron and Exon".
        """
        self.dataset.rename(
            columns={
                'CHROM': 'Chr',
                'POS': 'Pos',
                'REF': 'Ref',
                'ALT': 'Alt',
                'SYMBOL_SOURCE': 'SourceID',
                'Feature': 'FeatureID',
                'SYMBOL': 'GeneName',
                'INTRON': 'Intron',
                'EXON': 'Exon'
            }, inplace=True
        )
