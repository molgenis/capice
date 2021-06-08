from src.main.python.resources.annotaters.vep_processors.template import Template


class MotifEHIPos(Template):
    @classmethod
    @property
    def name(cls):
        return 'HIGH_INF_POS'

    @classmethod
    @property
    def usable(cls):
        return True

    @property
    def columns(self):
        return ['motifEHIPos']

    def process(self, value):
        return_value = 0
        if value[MotifEHIPos.name] == 'Y':
            return_value = 1
        return return_value
