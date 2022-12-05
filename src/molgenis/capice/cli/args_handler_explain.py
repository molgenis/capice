from molgenis.capice.main_explain import CapiceExplain
from molgenis.capice.core.capice_manager import CapiceManager
from molgenis.capice.cli.args_handler_parent import ArgsHandlerParent
from molgenis.capice.validators.model_validator import ModelValidator


class ArgsHandlerExplain(ArgsHandlerParent):
    """
    Handler for the CAPICE submodule Explain
    """

    def __init__(self, parser):
        super(ArgsHandlerExplain, self).__init__(parser=parser)

    @property
    def _extension(self):
        return '.json', '.ubj'

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
            help=f'path to trained model ({self._extension_str()}) (required)'
        )
        self.parser.add_argument(
            '-o',
            '--output',
            action='append',
            type=str,
            help=f'path to directory or file ({self._required_output_extensions_str()}) for '
                 f'exporting explain output (optional)'
        )
        self.parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            help='overwrites output if it already exists'
        )

    def _handle_module_specific_args(self, input_path, output_path, output_filename, output_given,
                                     args):
        model = self.load_model(input_path)
        validator = ModelValidator()
        validator.validate_has_required_attributes(model)
        CapiceManager().output_filename = output_filename
        CapiceExplain(model, output_path, output_given).run()
