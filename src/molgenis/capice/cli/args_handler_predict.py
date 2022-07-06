import pickle

from molgenis.capice import __version__
from molgenis.capice.main_predict import CapicePredict
from molgenis.capice.core.capice_manager import CapiceManager
from molgenis.capice.cli.args_handler_parent import ArgsHandlerParent
from molgenis.capice.validators.model_validator import ModelValidator
from molgenis.capice.validators.version_validator import VersionValidator


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
        return '.tsv.gz'

    @property
    def _empty_output_extension(self):
        return self._required_output_extensions

    def create(self):
        self.parser.add_argument(
            '-i',
            '--input',
            action='append',
            type=str,
            required=True,
            help='path to annotated variants file (.tsv or .tsv.gz) (required)'
        )
        self.parser.add_argument(
            '-m',
            '--model',
            action='append',
            type=str,
            required=True,
            help='path to trained model (.dat) (required)'
        )
        self.parser.add_argument(
            '-o',
            '--output',
            action='append',
            type=str,
            help='path to directory or filename (or both) for export. '
                 'If a filename is supplied, the filename has to have the .tsv.gz extension! '
                 '(optional)'
        )
        self.parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            help='overwrites output if it already exists'
        )

    def _handle_module_specific_args(self, input_path, output_path, output_filename, output_given,
                                     args):
        model_path = self.validate_length_one(args.model, '-m/--model')
        model = self.validate_model(model_path)
        CapiceManager().output_filename = output_filename
        CapicePredict(input_path, model, output_path, output_given).run()

    def validate_model(self, model_path):
        """
        Function to validate if the given model location is indeed a pickled
        model and matches the current CAPICE version.
        :param model_path: str, path-like, path to the model
        :return: model, xgb.XGBClassifier class
        """
        try:
            self.input_validator.validate_input_path(model_path, extension='.pickle.dat')
        except FileNotFoundError as cm:
            self.parser.error(str(cm))
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)
        model_validator = ModelValidator()
        model_validator.validate_is_xgb_classifier(model)
        model_validator.validate_has_required_attributes(model)
        version_validator = VersionValidator()
        try:
            version_validator.validate_model_version(model.CAPICE_version)
            version_validator.validate_versions_compatible(__version__, model.CAPICE_version)
        except ValueError as cm:
            self.parser.error(str(cm))
        return model
