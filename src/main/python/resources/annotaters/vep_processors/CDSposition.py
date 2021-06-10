from src.main.python.resources.annotaters.vep_processors.cDNAposition import CDNAPosition


class CDSPosition(CDNAPosition):
    @classmethod
    @property
    def name(cls):
        return 'CDS_position'

    @classmethod
    @property
    def usable(cls):
        return True

    @property
    def columns(self):
        return ['CDSpos', 'relCDSpos']
