from abc import ABCMeta, abstractmethod
import pandas as pd


class Template(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    @property
    def name(cls):
        return 'Template'

    @classmethod
    @abstractmethod
    @property
    def usable(cls):
        return False

    @abstractmethod
    def process(self, dataframe: pd.DataFrame):
        pass
