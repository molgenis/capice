from src.main.python.vep.template_sift_polyphen import TemplateSiftPolyPhen


class SIFT(TemplateSiftPolyPhen):
    def __init__(self):
        super(SIFT, self).__init__(
            name='SIFT',
            usable=True
        )

    @property
    def columns(self):
        return ['SIFTcat', 'SIFTval']
