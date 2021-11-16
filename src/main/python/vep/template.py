import pandas as pd
from abc import ABCMeta, abstractmethod
from src.main.python.validators.property_type_validator import PropertyTypeValidator


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
    def usable(self):
        return self._usable

    @usable.setter
    def usable(self, value=False):
        self.property_checker.validate_property(value=value, expected_type=bool)
        self._usable = value

    @property
    def drop(self):
        return True

    @abstractmethod
    def process(self, dataframe: pd.DataFrame):
        pass
