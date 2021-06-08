from src.main.python.resources.annotaters.vep_processors.template import Template


class SEQ(Template):
    @classmethod
    @property
    def name(cls):
        return 'Seq'

    @classmethod
    @property
    def usable(cls):
        return True

    @classmethod
    @property
    def columns(cls):
        return ['GC', 'CpG']

    def __init__(self):
        super().__init__()

    def process(self, seq):
        pass
