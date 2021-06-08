from src.main.python.core.logger import Logger
import pandas as pd


class ProcessorAnnotator:
    def __init__(self):
        self.log = Logger().logger
    pass

    @staticmethod
    def _col_renamer(dataframe: pd.DataFrame):
        """
        Function to rename "Gene, Feature, SYMBOL, INTRON and EXON" to
        "GeneID, FeatureID, GeneName, Intron and Exon".
        """
        dataframe.rename(
            columns={
                'Gene': 'GeneID',
                'Feature': 'FeatureID',
                'SYMBOL': 'GeneName',
                'INTRON': 'Intron',
                'EXON': 'Exon'
            }, inplace=True
        )
        return dataframe
