import pickle

from molgenis.capice import __version__
from molgenis.capice.main_explain import CapiceExplain
from molgenis.capice.core.capice_manager import CapiceManager
from molgenis.capice.utilities.input_processor import InputProcessor
from molgenis.capice.cli.args_handler_parent import ArgsHandlerParent
from molgenis.capice.validators.model_validator import ModelValidator
from molgenis.capice.validators.version_validator import VersionValidator


class ArgsHandlerExplain(ArgsHandlerParent):
    """
    Handler for the CAPICE submodule Explain
    """

    def __init__(self, parser):
        super(ArgsHandlerExplain, self).__init__(parser=parser)

    @property
    def _extension(self):
        return '.csv', '.csv.gz'

    @property
    def _required_output_extensions(self):
        return '.csv', '.csv.gz'

    @property
    def _empty_output_extension(self):
        return self._required_output_extensions[1]

    def create(self):
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
            help='path to directory or filename (or both) for export. '
                 'Has to be in .csv or .csv.gz extension. '
                 'Will always be gzipped!'
        )
        self.parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            help='overwrites output if it already exists'
        )

    def _handle_args(self, args):
        """
        Method overwrites the args_handler_parent because
        explain does not require an input argument.
        """
        try:
            VersionValidator().validate_capice_version(__version__)
        except ValueError as cm:
            self.parser.error(str(cm))
        input_path = self.validate_length_one(args.model, '-m/--model')
        try:
            self.input_validator.validate_input_path(input_path, extension='.pickle.dat')
        except FileNotFoundError as cm:
            self.parser.error(str(cm))
        output_path = None
        if args.output is not None:
            output_path = self.validate_length_one(args.output, '-o/--output')
        input_processor = InputProcessor(
            input_path=input_path,
            output_path=output_path,
            force=args.force,
            default_extension=self._empty_output_extension
        )
        output_filename = self._handle_output_filename(input_processor.get_output_filename())
        output_path = input_processor.get_output_directory()
        try:
            self.input_validator.validate_output_path(output_path)
        except OSError as cm:
            self.parser.error(str(cm))
        self._handle_module_specific_args(input_path, output_path, output_filename, args)

    def _handle_module_specific_args(self, input_path, output_path, output_filename, args):
        model_path = input_path
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)
        validator = ModelValidator()
        validator.validate_is_xgb_classifier(model)
        validator.validate_has_required_attributes(model)
        CapiceManager().output_filename = output_filename
        CapiceExplain(model, output_path).run()