import os
import pickle
import xgboost as xgb

from src.main_predict import Predict
from src.main.python.__version__ import __version__
from src.main.python.core.global_manager import CapiceManager
from src.main.python.cli.args_handler_parent import ArgsHandlerParent


class ArgsHandlerPredict(ArgsHandlerParent):
    """
    Child class ArgsHandlerPredict, specific to the predict part of CAPICE
    """

    def __init__(self, parser):
        super(ArgsHandlerPredict, self).__init__(parser=parser)

    @property
    def _extension(self):
        return '.tsv', '.tsv.gz'

    @property
    def _required_output_extensions(self):
        return '.tsv', '.tsv.gz'

    @property
    def _empty_output_extension(self):
        return self._required_output_extensions[0]

    def create(self):
        self.parser.add_argument(
            '-i',
            '--input',
            action='append',
            type=str,
            required=True,
            help='path to annotated variants file (.tsv or .tsv.gz)'
        )
        self.parser.add_argument(
            '-m',
            '--model',
            action='append',
            type=str,
            required=True,
            help='path to trained model (.dat)'
        )
        self.parser.add_argument(
            '-o',
            '--output',
            action='append',
            type=str,
            help='path to variant predictions file (.tsv or .tsv.gz)'
        )
        self.parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            help='overwrites output if it already exists'
        )

    def _handle_module_specific_args(
            self, input_loc, output_loc, output_filename, args):
        model_path = self.validate_length_one(args.model, '-m/--model')
        model = self.validate_model(model_path)
        if not output_filename.endswith('.gz'):
            output_filename = output_filename + '.gz'
        CapiceManager().output_filename = output_filename
        Predict(input_loc, model, output_loc).run()

    def validate_model(self, model_loc):
        """
        Function to validate if the given model location is indeed a pickled
        model and matches the current CAPICE version.
        :param model_loc: str, path-like, path to the model
        :return: model, xgb.XGBClassifier class
        """
        if not os.path.exists(model_loc):
            self.parser.error("Input model does not exist!")
        if not model_loc.endswith('.pickle.dat'):
            self.parser.error("Model does not have the right extension!")
        with open(model_loc, 'rb') as model_file:
            model = pickle.load(model_file)
        if not model.__class__ == xgb.XGBClassifier:
            self.parser.error("Given pickle is not a XGBClassifier class!")
        required_attributes = [
            'CAPICE_version',
            'impute_values',
            'predict_proba'
        ]
        for attribute in required_attributes:
            if attribute not in dir(model):
                self.parser.error(
                    f'Unable to locate attribute {attribute} in model file!'
                )
        if not model.CAPICE_version == __version__:
            self.parser.error(
                f'Model version {model.CAPICE_version} '
                f'does not match CAPICE version: {__version__}!'
            )
        return model
