import os
from src.main_train import Train
from src.main.python.core.cli.args_handler_parent import ArgsHandlerParent


class ArgsHandlerTrain(ArgsHandlerParent):
    """
    Command-line argument handler for train sub-command.
    Parses, validates and executes function.
    """

    def __init__(self, parser):
        super(ArgsHandlerTrain, self).__init__(parser=parser)

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
            nargs=1,
            type=str,
            required=True,
            help='path to classified annotated variants file (.tsv or .tsv.gz)'
        )
        self.parser.add_argument(
            '-m',
            '--impute',
            nargs=1,
            type=str,
            required=True,
            help='path to impute values file (.json)'
        )
        self.parser.add_argument(
            '-s',
            '--split',
            nargs=1,
            type=float,
            default=0.2,
            help='proportion of the input data to include '
                 'in the test split (default: %(default)s)'
        )
        self.parser.add_argument(
            '-o',
            '--output',
            nargs=1,
            type=str,
            help='path to model file (.dat)'
        )
        self.parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            help='overwrites output if it already exists'
        )

    def _handle_module_specific_args(
            self, input_loc, output_loc, output_filename, args):
        impute = args.impute[0]
        self.validate_input_json(impute)
        test_split = args.split
        # Since argparse doesn't cooperate well with default values and always
        # returns them as a list, this has to be done.
        if isinstance(test_split, list):
            test_split = test_split[0]
        self.validate_test_split(test_split)

        Train(input_loc, impute, test_split, output_loc).run()

    def validate_input_json(self, json_loc):
        """
        Function to validate that the impute json is present and has the
        correct extension.
        """
        if not os.path.exists(json_loc):
            self.parser.error('Input JSON does not exist!')
        if not json_loc.endswith('.json'):
            self.parser.error('Given input JSON is not a JSON file!')

    def validate_test_split(self, test_split):
        """
        Validator for test split to make sure it lies between 0 and 1
        (since the CLA is already set to type float, I do not have to validate
        it here too)
        """
        if test_split <= 0 or test_split >= 1:
            self.parser.error('Test split must be a float between 0 and 1')

