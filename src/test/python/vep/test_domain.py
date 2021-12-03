import unittest

import numpy as np
import pandas as pd

from src.main.python.vep import domain


class Domain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.cd = domain.Domain()

    def test_process_not_null(self):
        dataframe = pd.DataFrame({
            'DOMAINS': [
                'PROSITE_profiles:PS51085&PANTHER:PTHR11921:SF8&PANTHER:PTHR11921&TIGRFAM'
                ':TIGR00384&Pfam:PF13085&Gene3D:3.10.20.30&Superfamily:SSF54292',
                'PROSITE:PS51085&PANTHER:PTHR11921:SF8&PANTHER:PTHR11921&TIGRFAM:TIGR00384'
                '&Pfam:PF13085&Gene3D:3.10.20.30&Superfamily:SSF54292',
                'Coiled-coils_(Ncoils):PS51085&PROSITE_profiles:PS51085&PANTHER:PTHR11921:SF8'
                '&PANTHER:PTHR11921&TIGRFAM:TIGR00384&Pfam:PF13085&Gene3D:3.10.20.30'
                '&Superfamily:SSF54292',
                'Cleavage_site_(Signalp):blaat',
                'Low_complexity_(Seg):hello',
                'Bibbidibobbidiboo:poof']})
        observed = self.cd.process(dataframe)
        expected = pd.DataFrame({
            'DOMAINS': [
                'PROSITE_profiles:PS51085&PANTHER:PTHR11921:SF8&PANTHER:PTHR11921&TIGRFAM'
                ':TIGR00384&Pfam:PF13085&Gene3D:3.10.20.30&Superfamily:SSF54292',
                'PROSITE:PS51085&PANTHER:PTHR11921:SF8&PANTHER:PTHR11921&TIGRFAM:TIGR00384'
                '&Pfam:PF13085&Gene3D:3.10.20.30&Superfamily:SSF54292',
                'Coiled-coils_(Ncoils):PS51085&PROSITE_profiles:PS51085&PANTHER:PTHR11921:SF8'
                '&PANTHER:PTHR11921&TIGRFAM:TIGR00384&Pfam:PF13085&Gene3D:3.10.20.30'
                '&Superfamily:SSF54292',
                'Cleavage_site_(Signalp):blaat',
                'Low_complexity_(Seg):hello',
                'Bibbidibobbidiboo:poof'],
            'Domain': ['ndomain', 'hmmpanther', 'ncoils', 'sigp', 'lcompl', 'other']})
        pd.testing.assert_frame_equal(expected, observed)

    def test_process_null(self):
        dataframe = pd.DataFrame({'DOMAINS': [None, None]})
        observed = self.cd.process(dataframe)
        expected = pd.DataFrame({'DOMAINS': [None, None], 'Domain': [np.nan, np.nan]})
        pd.testing.assert_frame_equal(expected, observed)


if __name__ == '__main__':
    unittest.main()
