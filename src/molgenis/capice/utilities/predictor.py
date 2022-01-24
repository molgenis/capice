from molgenis.capice.core.logger import Logger
from molgenis.capice.utilities.enums import Column


class Predictor:
    """
    Predictor class for CAPICE. Produces the final CAPICE score.
    """

    def __init__(self, model):
        """
        :param model: XGBClassifier, the custom pickled model instance of user
        provided model.
        """
        self.log = Logger().logger
        self.model = model
        self.log.info('Starting prediction.')

    def predict(self, dataset):
        """
        Predicts the probability score of CAPICE over dataset.
        :param dataset: pandas.DataFrame, the fully imputed and processed
        user input dataset of VEP-like origin.
        :return: pandas.DataFrame: containing an extra column containing the
        CAPICE score per variant.
        """
        self.log.info('Predicting for %d samples.', dataset.shape[0])
        dataset[Column.score.value] = self.model.predict_proba(
            dataset[self.model.get_booster().feature_names])[:, 1]
        self.log.info('Prediction successful.')
        return dataset
