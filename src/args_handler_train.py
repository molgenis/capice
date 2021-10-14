from args_handler_subparser import ArgsHandlerSubparser
from src.trainer import Trainer


class ArgsHandlerTrain(ArgsHandlerSubparser):
    """
    Command-line argument handler for train sub-command.
    Parses, validates and executes function.
    """
    KEYWORDS_INPUT = ('-i', '--input')
    KEYWORDS_IMPUTE = ('-m', '--impute')
    KEYWORDS_SPLIT = ('-s', '--split')
    KEYWORDS_OUTPUT = ('-o', '--output')
    KEYWORDS_FORCE = ('-f', '--force')

    ACCEPTED_EXTENSION_OUTPUT = ('.pickle.dat',)
    SPLIT_DEFAULT = 0.2

    def create(self):
        self.parser.add_argument(
            self.KEYWORDS_INPUT[0],
            self.KEYWORDS_INPUT[1],
            action='append',
            type=str,
            required=True,
            help='path to classified annotated variants file (.tsv or .tsv.gz)'
        )
        self.parser.add_argument(
            self.KEYWORDS_IMPUTE[0],
            self.KEYWORDS_IMPUTE[1],
            action='append',
            type=str,
            required=True,
            help='path to impute values file (.json)'
        )
        self.parser.add_argument(
            self.KEYWORDS_SPLIT[0],
            self.KEYWORDS_SPLIT[1],
            action='append',
            type=float,
            help='proportion of the input data to include '
                 'in the test split (default: %(default)s)'
        )
        self.parser.add_argument(
            self.KEYWORDS_OUTPUT[0],
            self.KEYWORDS_OUTPUT[1],
            action='append',
            type=str,
            help='path to model file (.dat)'
        )
        self.parser.add_argument(
            self.KEYWORDS_FORCE[0],
            self.KEYWORDS_FORCE[1],
            action='store_true',
            help='overwrites output if it already exists'
        )

    def _handle_args(self, args):
        # Digest input path.
        input_path = self._validate_argument_max_once(self.KEYWORDS_INPUT,
                                                      args.input)
        input_path = self._validate_file(input_path, ['.tsv', '.tsv.gz'])

        # Digest impute path.
        impute_path = self._validate_argument_max_once(self.KEYWORDS_IMPUTE,
                                                       args.impute)
        impute_path = self._validate_file(impute_path, ['.json'])

        # Digest split.
        test_split = self._validate_argument_max_once(self.KEYWORDS_SPLIT,
                                                      args.split)
        if test_split is None:
            test_split = self.SPLIT_DEFAULT
        else:
            test_split = self._validate_range(self.KEYWORDS_SPLIT, test_split,
                                              (0, 1))

        # Digest output path.
        output_path = self._validate_argument_max_once(self.KEYWORDS_OUTPUT,
                                                       args.output)
        output_path = self.\
            _generate_path_dynamically(output_path, input_path,
                                       self.ACCEPTED_EXTENSION_OUTPUT,
                                       self.ACCEPTED_EXTENSION_OUTPUT[0])
        self._validate_force_exists(output_path, args.force)

        # Run trainer.
        print(input_path)
        print(impute_path)
        print(test_split)
        print(output_path)
        # Trainer(input_path, impute_path, test_split, output_path).train()
