import unittest

import os
import pickle
import xgboost as xgb

from tests.capice.test_templates import _project_root_directory
from molgenis.capice.validators.model_validator import ModelValidator


class TestModelValidator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = ModelValidator()
        with open(
                os.path.join(
                    _project_root_directory,
                    'tests',
                    'resources',
                    'xgb_booster_poc.pickle.dat'
                ), 'rb'
        ) as model_file:
            cls.model = pickle.load(model_file)

    def test_model_type_correct(self):
        self.validator.validate_is_xgb_classifier(self.model)

    def test_model_required_attributes_correct(self):
        self.validator.validate_has_required_attributes(self.model)

    def test_model_type_incorrect(self):
        model = self.model.get_booster()
        self.assertRaises(
            TypeError,
            self.validator.validate_is_xgb_classifier,
            model
        )

    def test_model_missing_attribute(self):
        model = xgb.XGBClassifier()
        self.assertRaises(
            AttributeError,
            self.validator.validate_has_required_attributes,
            model
        )


if __name__ == '__main__':
    unittest.main()
