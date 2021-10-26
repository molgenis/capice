from main.python.resources.Validators import PostVEPProcessingValidator
from main.python.resources.predictors.Predictor import Predictor
from main_capice import Main


class Predict(Main):
    """
    Predict class of CAPICE to call the different modules to impute,
    preprocess and eventually predict a score over a CAPICE annotated file.
    """
    def __init__(self, input_loc, model, output_loc):
        super().__init__()

        # Input file.
        self.infile = input_loc
        self.log.debug('Input argument -i / --input confirmed: %s',
                       self.infile)

        # Model.
        self.model = model

        # Output file.
        self.output = output_loc
        self.log.debug(
            'Output directory -o / --output confirmed: %s', self.output
        )

        # Force flag.
        self.log.debug('Force flag confirmed: %s', self.manager.force)

    def run(self):
        """
        Function to make CAPICE run in a prediction matter.
        """
        capice_data = self.load_file(infile=self.infile)
        capice_data = self.process(loaded_data=capice_data)
        capice_data = self.impute(loaded_data=capice_data,
                                  model=self.model)
        capice_data = self.preprocess(loaded_data=capice_data,
                                      model=self.model)
        capice_data = self.predict(loaded_data=capice_data)
        self._export(dataset=capice_data, output=self.output)

    def process(self, loaded_data):
        """
        Function to process the VEP file to a CAPICE file
        """
        processed_data = super().process(loaded_data)
        validator = PostVEPProcessingValidator(self.model)
        validator.validate_features_present(processed_data)
        return processed_data

    def predict(self, loaded_data):
        """
        Function to call the correct model to predict CAPICE scores
        :return: pandas DataFrame
        """
        predictor = Predictor(self.model)
        capice_data = predictor.predict(loaded_data)
        return capice_data
