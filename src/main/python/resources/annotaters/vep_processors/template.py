from abc import ABCMeta, abstractmethod


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

    @classmethod
    @abstractmethod
    @property
    def columns(cls):
        return []

    def __init__(self):
        pass

    @abstractmethod
    def process(self, value):
        pass
