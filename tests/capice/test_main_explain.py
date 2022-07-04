import unittest

import os
import pickle

import pandas as pd

from tests.capice.test_templates import _project_root_directory
from molgenis.capice.core.capice_manager import CapiceManager
from molgenis.capice.main_explain import CapiceExplain


class TestCapiceExplain(unittest.TestCase):
    output_path = os.path.join(_project_root_directory, 'testing_output')
    output_filename = 'test_output.csv.gz'
    full_output_path = os.path.join(output_path, output_filename)

    @classmethod
    def setUpClass(cls) -> None:
        with open(
            os.path.join(
                _project_root_directory,
                'tests',
                'resources',
                'xgb_booster_poc.pickle.dat'
            ), 'rb'
        ) as model_file:
            cls.model = pickle.load(model_file)
        if not os.path.isdir(cls.output_path):
            os.makedirs(cls.output_path)
        CapiceManager().output_filename = cls.output_filename

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.isfile(cls.full_output_path):
            os.remove(cls.full_output_path)
        if os.path.isdir(cls.output_path):
            os.rmdir(cls.output_path)

    def test_capice_explain(self):
        explainer = CapiceExplain(model=self.model, output_path=self.output_path)
        explainer.run()
        feature_importances = self.model.get_booster().get_score(importance_type='gain')
        observed = pd.read_csv(self.full_output_path, sep='\t')
        expected = pd.DataFrame(
            data=[
                feature_importances.keys(),
                feature_importances.values()
            ], index=['feature', 'gain']
        ).T.sort_values(by='gain', ascending=False).reset_index(drop=True)
        expected['gain'] = expected['gain'].astype(float)
        expected['total_gain'] = expected['feature'].map(self.model.get_booster().get_score(
            importance_type='total_gain'))
        expected['weight'] = expected['feature'].map(self.model.get_booster().get_score(
            importance_type='weight'))
        expected['cover'] = expected['feature'].map(self.model.get_booster().get_score(
            importance_type='cover'))
        expected['total_cover'] = expected['feature'].map(self.model.get_booster().get_score(
            importance_type='total_cover'))
        print(expected)
        print(observed)
        pd.testing.assert_frame_equal(observed, expected)


if __name__ == '__main__':
    unittest.main()
