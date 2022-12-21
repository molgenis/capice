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
    def _model_extension(self) -> tuple[str]:
        # Ignore because the amount of values of tuple does not matter.
        return '.json', '.ubj'  # type: ignore

    def _model_extension_str(self) -> str:
        return self._join_extensions(self._model_extension)

    @property
    def _required_output_extensions(self):
        return '.tsv', '.tsv.gz'

    @property
    def _empty_output_extension(self):
        return self._required_output_extensions[1]

    def create(self):
        self.parser.add_argument(
            '-i',
            '--input',
            action='append',
            type=str,
            required=True,
            help=f'path to annotated variants file ({self._extension_str()}) (required)'
        )
        self.parser.add_argument(
            '-m',
            '--model',
            action='append',
            type=str,
            required=True,
            help=f'path to trained model ({self._model_extension_str()}) (required)'
        )
        self.parser.add_argument(
            '-o',
            '--output',
            action='append',
            type=str,
            help=f'path to directory or file ({self._required_output_extensions_str()}) '
                 f'for exporting prediction output (optional)'
        )
        self.parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            help='overwrites output if it already exists'
        )

    def _handle_module_specific_args(self, input_path, output_path, output_filename, output_given,
                                     args):
        model_path = self._retrieve_argument_from_list(args.model, '-m/--model')
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
            self.input_validator.validate_input_path(model_path, extension=self._model_extension)
        except FileNotFoundError as cm:
            self.parser.error(str(cm))
        model = self.load_model(model_path)
        model_validator = ModelValidator()
        model_validator.validate_has_required_attributes(model)
        version_validator = VersionValidator()
        try:
            version_validator.validate_model_version(model.CAPICE_version)
            version_validator.validate_versions_compatible(__version__, model.CAPICE_version)
        except ValueError as cm:
            self.parser.error(str(cm))
        return model
