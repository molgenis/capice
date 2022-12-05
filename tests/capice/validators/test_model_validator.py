import unittest

import xgboost as xgb

from tests.capice.test_templates import TestResource, load_model
from molgenis.capice.validators.model_validator import ModelValidator


class TestModelValidator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = ModelValidator()
        cls.model = load_model(TestResource.XGB_BOOSTER_POC_UBJ.value)

    def test_model_required_attributes_correct(self):
        self.validator.validate_has_required_attributes(self.model)

    def test_model_missing_attribute(self):
        model = xgb.XGBClassifier()
        self.assertRaises(
            AttributeError,
            self.validator.validate_has_required_attributes,
            model
        )


if __name__ == '__main__':
    unittest.main()
