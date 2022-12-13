from molgenis.capice.main_train import CapiceTrain
from molgenis.capice.core.capice_manager import CapiceManager
from molgenis.capice.cli.args_handler_parent import ArgsHandlerParent


class ArgsHandlerTrain(ArgsHandlerParent):
    """
    Command-line argument handler for train sub-command.
    Parses, validates and executes function.
    """

    def __init__(self, parser):
        super(ArgsHandlerTrain, self).__init__(parser=parser)
        self.split_default = 0.2
        self.n_threads_default = 1

    @property
    def _extension(self):
        return '.tsv', '.tsv.gz'

    @property
    def _features_extension(self) -> tuple[str]:
        return '.json',

    def _features_extension_str(self) -> str:
        return self._join_extensions(self._features_extension)

    @property
    def _required_output_extensions(self):
        return '.json', '.ubj'

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
            '-e',
            '--features',
            action='append',
            type=str,
            required=True,
            help=f'path to the features file ({self._features_extension_str()}) (required)'
        )
        self.parser.add_argument(
            '-s',
            '--split',
            action='append',
            default=[self.split_default],
            type=float,
            help=f'proportion of the input data to include in the test split (default: '
                 f'{self.split_default}) (optional)'
        )
        self.parser.add_argument(
            '-o',
            '--output',
            action='append',
            type=str,
            help=f'path to directory or file ({self._required_output_extensions_str()}) for '
                 f'exporting model (optional)'
        )
        self.parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            help='overwrites output if it already exists'
        )
        self.parser.add_argument(
            '-t',
            '--threads',
            action='append',
            default=[self.n_threads_default],
            type=int,
            help=f'The amount of threads that can be used by XGBoost to parallel train (default: '
                 f'{self.n_threads_default})'
        )

    def _handle_module_specific_args(self, input_path, output_path, output_filename, output_given,
                                     args):
        features = self._retrieve_argument_from_list(args.features, '-e/--features')
        self.input_validator.validate_input_path(features, extension=self._features_extension)

        test_split = self._retrieve_argument_from_list(args.split, '-s/--split', has_default=True)
        self.validate_test_split(test_split)

        n_threads = self._retrieve_argument_from_list(args.threads, '-t/--threads',
                                                      has_default=True)
        self.validate_n_threads(n_threads)

        CapiceManager().output_filename = output_filename
        CapiceTrain(input_path, features, test_split, output_path, output_given, n_threads).run()

    def validate_n_threads(self, n_threads):
        """
        Function to validate that the amount of threads is at least 1.
        """
        if n_threads < 1:
            self.parser.error('The amount of threads has to be at least 1!')

    def validate_test_split(self, test_split):
        """
        Validator for test split to make sure it lies between 0 and 1
        (since the CLA is already set to type float, I do not have to validate
        it here too)
        """
        if test_split <= 0 or test_split >= 1:
            self.parser.error('Test split must be a float between 0 and 1')
