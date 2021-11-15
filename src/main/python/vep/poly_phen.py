from src.main.python.vep.template_sift_polyphen import TemplateSiftPolyPhen


class PolyPhen(TemplateSiftPolyPhen):
    def __init__(self):
        super(PolyPhen, self).__init__(
            name='PolyPhen',
            usable=True
        )

    @property
    def columns(self):
        return ['PolyPhenCat', 'PolyPhenVal']
