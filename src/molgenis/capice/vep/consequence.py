import numpy as np
import pandas as pd

from molgenis.capice.core.logger import Logger
from molgenis.capice.vep.template import Template


class Consequence(Template):
    def __init__(self):
        super(Consequence, self).__init__(
            name='Consequence',
            usable=True
        )
        self.log = Logger().logger

    @property
    def drop(self):
        return True

    @property
    def columns(self):
        return ['most_severe_consequence']

    @property
    def dtypes(self) -> list[str]:
        return ['category']

    @staticmethod
    def _fillna():
        return 0

    def _process(self, dataframe: pd.DataFrame):
        dataframe[self.columns[0]] = dataframe[self.name].str.split('&').str[0]
        return dataframe
