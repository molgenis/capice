from src.main.python.core.logger import Logger
from src.main.python.resources.enums.sections import Column


class Predictor:
    def __init__(self, model):
        self.log = Logger().logger
        self.model = model
        self.log.info('Starting prediction.')

    def predict(self, dataset):
        self.log.info('Predicting for %d samples.', dataset.shape[0])
        dataset[Column.score.value] = self.model.predict_proba(
            dataset[self.model.get_booster().feature_names]
        )[:, 1]
        self.log.info('Prediction successful.')
        return dataset
