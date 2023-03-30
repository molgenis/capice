import pandas as pd

from molgenis.capice.core.logger import Logger
from molgenis.capice.utilities.enums import InputColumn


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
        to_rename = {}
        for column in InputColumn:
            if column.col_input_name in self.dataset.columns:
                to_rename[column.col_input_name] = column.col_name
        self.log.debug(f'Converting the following column names: {to_rename}')
        self.dataset.rename(columns=to_rename, inplace=True)
