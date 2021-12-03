import pandas as pd

from src.main.python.core.logger import Logger
from src.main.python.utilities.enums import Column


class LoadFilePostProcessor:
    def __init__(self, dataset: pd.DataFrame):
        self.log = Logger().logger
        self.dataset = dataset

    def process(self):
        """
        Function to start the LoadFilePostProcessor to correct the input file of
        each column starting with % and the renaming of certain columns,
        like #CHROM to chr.

        Returns
        -------
        dataset :   pandas.DataFrame
                    Processed dataset with corrected % sign and renamed columns.
        """
        self.log.debug('Starting correcting % sign.')
        self._correct_percentage_sign()
        self.log.debug('% sign corrected, starting renaming of columns.')
        self._col_renamer()
        self.log.info('LoadFilePostProcessor successful.')
        return self.dataset

    def _correct_percentage_sign(self):
        new_columns = []
        for column in self.dataset.columns:
            if column.startswith('%'):
                new_columns.append(column.split('%')[1])
            elif column.startswith('#'):
                new_columns.append(column.split('#')[1])
            else:
                new_columns.append(column)
        self.dataset.columns = new_columns

    def _col_renamer(self):
        """
        Function to rename "Gene, Feature, SYMBOL, INTRON and EXON" to
        "GeneID, FeatureID, GeneName, Intron and Exon".
        """
        self.dataset.rename(
            columns={'CHROM': Column.chr.value,
                     'POS': Column.pos.value,
                     'REF': Column.ref.value,
                     'ALT': Column.alt.value,
                     'HGNC_ID': Column.gene_id.value,
                     'SYMBOL_SOURCE': Column.id_source.value,
                     'Feature': Column.transcript.value,
                     'SYMBOL': Column.gene_name.value,
                     'INTRON': 'Intron',
                     'EXON': 'Exon',
                     'MAX_AF': 'max_AF'},
            inplace=True)
