from src.main.python.resources.annotaters.vep_processors.cDNAposition import CDNAPosition


class ProteinPosition(CDNAPosition):
    @classmethod
    @property
    def name(cls):
        return 'Protein_position'

    @classmethod
    @property
    def usable(cls):
        return True

    @property
    def columns(self):
        return ['protPos', 'relProtPos']

    @property
    def get_name(self):
        return ProteinPosition.name
