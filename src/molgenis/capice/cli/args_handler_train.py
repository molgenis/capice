import os

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

    @property
    def _extension(self):
        return '.tsv.gz', '.tsv'

    @property
    def _required_output_extensions(self):
        return '.pickle.dat'

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
            help='path to classified annotated variants file (.tsv or .tsv.gz) (required)'
        )
        self.parser.add_argument(
            '-m',
            '--impute',
            action='append',
            type=str,
            required=True,
            help='path to impute values file (.json) (required)'
        )
        self.parser.add_argument(
            '-s',
            '--split',
            action='append',
            type=float,
            help='proportion of the input data to include in the test split (default: %('
                 'default)s) (optional)'
        )
        self.parser.add_argument(
            '-o',
            '--output',
            action='append',
            type=str,
            help='path to directory or filename (or both) for export. '
                 'If a filename is supplied, the filename has to have the .pickle.dat extension! '
                 '(optional)'
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
            action='store',
            default=1,
            type=int,
            help='The amount of threads that can be used by XGBoost to parallel train (default: '
                 '%(default)s)'
        )

    def _handle_module_specific_args(self, input_path, output_path, output_filename, output_given,
                                     args):
        impute = self.validate_length_one(args.impute, '-m/--impute')
        self.validate_input_json(impute)
        test_split = self.validate_length_one(args.split, '-s/--split')
        if test_split is None:
            test_split = self.split_default
        # Since argparse doesn't cooperate well with default values and always
        # returns them as a list, this has to be done.
        if isinstance(test_split, list):
            test_split = test_split[0]
        self.validate_test_split(test_split)
        n_threads = args.threads
        self.validate_n_threads(n_threads)
        CapiceManager().output_filename = output_filename
        CapiceTrain(input_path, impute, test_split, output_path, output_given, n_threads).run()

    def validate_input_json(self, json_path):
        """
        Function to validate that the impute json is present and has the
        correct extension.
        """
        if not os.path.exists(json_path):
            self.parser.error('Input JSON does not exist!')
        if not json_path.endswith('.json'):
            self.parser.error('Given input JSON is not a JSON file!')

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

