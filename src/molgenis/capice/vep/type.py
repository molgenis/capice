import pandas as pd

from molgenis.capice.utilities.enums import Column
from molgenis.capice.vep.template import Template


class Type(Template):
    def __init__(self):
        super(Type, self).__init__(
            name=Column.ref.value,
            usable=True
        )

    @property
    def columns(self):
        return ['Type']

    @staticmethod
    def _ensure_column_value_is_one(column):
        return column.str.len() == 1

    def _process(self, dataframe: pd.DataFrame):
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
        alt_column = dataframe[Column.alt.value]
        ref_column = dataframe[Column.ref.value]

        alt_column_value_is_1 = self._ensure_column_value_is_one(alt_column)
        ref_column_value_is_1 = self._ensure_column_value_is_one(ref_column)

        first_ref_nuc = ref_column.str.get(0)
        first_alt_nuc = alt_column.str.get(0)

        dataframe[self.columns] = 'DELINS'
        dataframe.loc[
            dataframe[ref_column_value_is_1 & alt_column_value_is_1].index, self.columns] = 'SNV'
        dataframe.loc[
            dataframe[
                (first_ref_nuc == alt_column) & alt_column_value_is_1].index, self.columns] = 'DEL'
        dataframe.loc[
            dataframe[
                (first_alt_nuc == ref_column) & ref_column_value_is_1].index, self.columns] = 'INS'
        return dataframe

    @property
    def drop(self):
        return False
