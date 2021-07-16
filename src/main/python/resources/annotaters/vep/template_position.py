from src.main.python.resources.annotaters.vep.template import Template
import pandas as pd


class TemplatePosition(Template):
    def __init__(self, name='Template', usable=False):
        super(TemplatePosition, self).__init__(
            name=name,
            usable=usable
        )

    @property
    def columns(self):
        return [None, None]

    @property
    def pos_col(self):
        return self.columns[0]

    def process(self, dataframe: pd.DataFrame):
        dataframe[self.columns] = dataframe[self.name].str.split(
            '/',
            expand=True
        )
        dataframe[self.pos_col] = dataframe[self.pos_col].str.replace(
            '?-',
            '',
            regex=False
        )
        dataframe[self.pos_col] = dataframe[self.pos_col].str.replace(
            '-?',
            '',
            regex=False
        )
        dataframe[self.pos_col] = dataframe[self.pos_col].str.split(
            '-', expand=True)[0]
        for column in self.columns:
            dataframe[column] = dataframe[column].astype(float)
        return dataframe
