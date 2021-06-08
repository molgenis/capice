from src.main.python.resources.annotaters.vep_processors.template import Template


class MotifEScoreChange(Template):
    @classmethod
    def name(cls):
        return 'MOTIF_SCORE_CHANGE'

    @classmethod
    def usable(cls):
        return True

    @property
    def columns(self):
        return ['motifEScoreChng']

    def process(self, value):
        return value[MotifEScoreChange.name]
