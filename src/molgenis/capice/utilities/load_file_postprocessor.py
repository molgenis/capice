import pandas as pd

from molgenis.capice.core.logger import Logger
from molgenis.capice.utilities.enums import Column


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
        self.log.info('LoadFilePostProcessor starting.')
        self._col_renamer()
        self.log.info('LoadFilePostProcessor successful.')
        return self.dataset

    def _col_renamer(self):
        """
        Function to rename "Gene, Feature, SYMBOL, INTRON and EXON" to
        "GeneID, FeatureID, GeneName, Intron and Exon".
        """
        self.dataset.rename(
            columns={'CHROM': Column.chr.value,
                     'POS': Column.pos.value,
                     'Gene': Column.gene_id.value,
                     'SYMBOL_SOURCE': Column.id_source.value,
                     'Feature': Column.feature.value,
                     'Feature_type': Column.feature_type.value,
                     'SYMBOL': Column.gene_name.value,
                     'INTRON': 'Intron',
                     'EXON': 'Exon',
                     'MAX_AF': 'max_AF'},
            inplace=True)
