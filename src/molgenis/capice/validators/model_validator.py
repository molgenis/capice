import xgboost


class ModelValidator:
    @staticmethod
    def validate_is_xgb_classifier(model):
        """
        Function to validate if loaded pickle is of xgb.XGBClassifier class.
        """
        if not isinstance(model, xgboost.XGBClassifier):
            raise TypeError('Given pickle is not a XGBClassifier class!')

    @staticmethod
    def validate_has_required_attributes(model):
        """
        Function to validate if the required attributes CAPICE_version,
        impute_values and predict_proba are present.
        """
        required_attributes = ['CAPICE_version', 'impute_values', 'predict_proba']
        for attribute in required_attributes:
            if attribute not in dir(model):
                raise AttributeError(f'Unable to locate attribute {attribute} in model file!')
