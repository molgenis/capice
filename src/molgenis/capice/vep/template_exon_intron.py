from abc import abstractmethod

import pandas as pd

from molgenis.capice.vep.template import Template


class TemplateExonIntron(Template):
    def __init__(self, name='Template', usable=False):
        super(TemplateExonIntron, self).__init__(
            name=name,
            usable=usable
        )

    @property
    @abstractmethod
    def columns(self):
        return [None, None]

    @property
    def get_number_column(self):
        return self.columns[0]

    @property
    def get_number_affected_column(self):
        return self.columns[1]

    @property
    def get_total_column(self):
        return self.columns[2]

    def _calculate_affected(self, dataframe):
        # Checking if any is InDel affecting multiple exons/intron (True) or if only SNV (False)
        if dataframe[self.get_number_column].str.contains('-', regex=False).any():
            # Obtain the last affected intron/exon
            dataframe['temp_column'] = dataframe[self.get_number_column].str.split(
                '-', expand=True
            )[1]
            # Obtain the first affected intron/exon
            dataframe[self.get_number_column] = dataframe[self.get_number_column].str.split(
                '-', expand=True
            )[0]
            # Ensuring math can be performed
            for col in ['temp_column', self.get_number_column]:
                dataframe[col] = dataframe[col].astype('Int64')
            # Performing math (+1 because all affected columns have to be included)
            dataframe[self.get_number_affected_column] = abs(
                dataframe[self.get_number_column] - dataframe['temp_column']
            ) + 1
            # Fill where intron/exon number is not NaN with 1 if SNV
            dataframe.loc[
                (
                        dataframe[self.get_number_column].notnull() &
                        dataframe[self.get_number_affected_column].isnull()
                ),
                self.get_number_affected_column
            ] = 1
            dataframe.drop(columns=['temp_column'], inplace=True)
        else:
            # Setting every SNV that has an intron/exon to affected = 1
            dataframe.loc[dataframe[self.name].notnull(), self.get_number_affected_column] = 1

    def _process(self, dataframe: pd.DataFrame):
        dataframe[
            [self.get_number_column, self.get_total_column]
        ] = dataframe[self.name].str.split('/', expand=True)
        self._calculate_affected(dataframe)
        for column in self.columns:
            dataframe[column] = dataframe[column].astype('Int64')
        return dataframe
