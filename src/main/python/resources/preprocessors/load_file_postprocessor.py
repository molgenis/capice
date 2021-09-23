import pandas as pd
import logging
logger = logging.getLogger(__name__)


class LoadFilePostProcessor:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset

    def process(self):
        """
        Function to start the LoadFilePostProcessor to correct the input file of
        each column starting with % and the renaming of certain columns,
        like #CHROM to Chr.

        Returns
        -------
        dataset :   pandas.DataFrame
                    Processed dataset with corrected % sign and renamed columns.
        """
        logger.debug('Starting correcting % sign.')
        self._correct_percentage_sign()
        logger.debug('% sign corrected, starting renaming of columns.')
        self._col_renamer()
        self._correct_dtypes()
        logger.info('LoadFilePostProcessor successful.')
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

    def _correct_dtypes(self):
        self.dataset['Chr'] = self.dataset['Chr'].astype(str)

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
                'HGNC_ID': 'gene_id',
                'SYMBOL_SOURCE': 'id_source',
                'Feature': 'transcript',
                'SYMBOL': 'gene_name',
                'INTRON': 'Intron',
                'EXON': 'Exon',
                'MAX_AF': 'max_AF'
            }, inplace=True
        )
