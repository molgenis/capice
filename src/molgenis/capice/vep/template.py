from abc import ABCMeta, abstractmethod

import numpy as np
import pandas as pd

from molgenis.capice.validators.property_type_validator import PropertyTypeValidator


class Template(metaclass=ABCMeta):
    def __init__(self, name, usable):
        self.property_checker = PropertyTypeValidator()
        self.name = name
        self.usable = usable

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value='Template'):
        self.property_checker.validate_property(value=value, expected_type=str)
        self._name = value

    @property
    @abstractmethod
    def columns(self):
        return []

    @property
    def usable(self):
        return self._usable

    @usable.setter
    def usable(self, value=False):
        self.property_checker.validate_property(value=value, expected_type=bool)
        self._usable = value

    @property
    def drop(self):
        return True

    @staticmethod
    def _fillna():
        return np.nan

    def process(self, dataframe: pd.DataFrame):
        if dataframe[self.name].isnull().all():
            dataframe[self.columns] = self._fillna()
            return dataframe
        else:
            return self._process(dataframe)

    @abstractmethod
    def _process(self, dataframe: pd.DataFrame):
        return dataframe
