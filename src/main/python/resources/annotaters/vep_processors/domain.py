import pandas as pd
from src.main.python.resources.annotaters.vep_processors.template import Template
import numpy as np


class Domain(Template):
    """
    This class contains a lot of complex Pandas codebase, allow me to explain here:

    First the column Domain.name is split on the '&' character, each split gets it's own column due to expand=True.
    Then another split happens on ":" to split the source from the name, where only the source is kept.
    Then the function process_ndomain is called to set the index value 3 to any column that contains the characters:
    '_domain' or '_profile', given that they are not NaN. If a column does not contain the characters, the value is
    left unchanged.
    Then I know that the remaining terms should directly match every key in the property levels_dict, so a direct
    replace is called for that.
    The tricky part is then to mark everything that is left and not NaN as 5, which is what the function process_others
    does. It looks if a value is 1. not NaN, 2. not within the levels_dict keys and 3. not within the levels_dict
    values. Anything that is left "True" after these 3 filters is set to 5.
    Finally the index numbers are aggregated over the columns with the 'min' function, mapped back to the string and
    applied.
    """
    def __init__(self):
        super(Domain, self).__init__(
            name='DOMAINS',
            usable=True
        )

    @property
    def columns(self):
        return ['Domain']

    @property
    def levels_dict(self):
        return {'PANTHER': 4, 'ndomain': 3, 'Low_complexity_(Seg)': 2, 'Cleavage_site_(Signalp)': 1,
                'Coiled-coils_(Ncoils)': 0}

    @property
    def output_dict(self):
        return {0.0: 'ncoils', 1.0: 'sigp', 2.0: 'lcompl', 3.0: 'ndomain', 4.0: 'hmmpanther', 5.0: 'other'}

    def process(self, dataframe: pd.DataFrame):
        subset = dataframe[self.name].str.split('&', expand=True)
        subset = subset.apply(lambda x: x.str.split(':', expand=True)[0], axis=0)
        subset = self.process_ndomain(subset)
        subset.replace(self.levels_dict, inplace=True)
        subset = self.process_others(subset)
        subset = subset.agg('min', axis=1)
        subset.replace(self.output_dict, inplace=True)
        dataframe[self.columns] = subset
        return dataframe

    @staticmethod
    def process_ndomain(subset: pd.DataFrame):
        for col in subset.columns:
            subset[col] = np.where(subset[col].str.contains('_domain') & subset[col].notnull(), 3, subset[col])
            subset[col] = np.where(subset[col].str.contains('_profile') & subset[col].notnull(), 3, subset[col])
        return subset

    def process_others(self, subset: pd.DataFrame):
        for col in subset.columns:
            subset[col] = np.where(
                subset[col].notnull() & ~subset[col].isin(self.levels_dict.keys()) & ~subset[col].isin(
                    self.levels_dict.values()), 5, subset[col])
        return subset
