import pandas as pd
from src.main.python.vep.template import Template
from src.main.python.utilities.enums import Column


class Type(Template):
    def __init__(self):
        super(Type, self).__init__(
            name=Column.ref.value,
            usable=True
        )

    def process(self, dataframe: pd.DataFrame):
        """
        process variants to annotate their types
        :param dataframe: a dataframe with as columns at least a ref and an alt
        :return: a dataframe with an added types column

        if len(ref) == 1 && len (alt) == 1:
            type = 'SNV'
        elif ref[0] == alt &&  len(alt) == 1:
            type = 'DEL'
        elif alt[0] == ref && len(ref) == 1:
            type = 'INS'
        else:
            type = 'DELINS'
        """
        dataframe['Type'] = 'DELINS'
        dataframe.loc[
            dataframe[
                (dataframe[Column.ref.value].str.len() == 1) & (
                            dataframe[Column.alt.value].str.len() == 1)].index, 'Type'] = 'SNV'
        dataframe.loc[
            dataframe[
                (dataframe[Column.ref.value].str.get(0) == dataframe[Column.alt.value]) & (
                        dataframe[Column.alt.value].str.len() == 1)].index, 'Type'] = 'DEL'
        dataframe.loc[
            dataframe[
                (dataframe[Column.alt.value].str.get(0) == dataframe[Column.ref.value]) & (
                        dataframe[Column.ref.value].str.len() == 1)].index, 'Type'] = 'INS'
        return dataframe

    @property
    def drop(self):
        return False
