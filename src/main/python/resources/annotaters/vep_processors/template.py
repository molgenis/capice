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

    @abstractmethod
    @property
    def columns(self):
        return []

    @property
    def delete_after(self):
        return True

    @abstractmethod
    def process(self, value):
        pass
