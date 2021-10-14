from args_handler_subparser import ArgsHandlerSubparser
from src.predicter import Predicter


class ArgsHandlerPredict(ArgsHandlerSubparser):
    """
    Command-line argument handler for predict sub-command.
    Parses, validates and executes function.
    """
    KEYWORDS_INPUT = ('-i', '--input')
    KEYWORDS_MODEL = ('-m', '--model')
    KEYWORDS_OUTPUT = ('-o', '--output')
    KEYWORDS_FORCE = ('-f', '--force')

    ACCEPTED_EXTENSIONS_TSV = ('.tsv', '.tsv.gz')

    def __init__(self, parser):
        super().__init__(parser)

    def create(self):
        """
        Classmethod create for ArgsHandlerPredict, to create arguments specific
        to the Predict module of CAPICE. Will return an initialized instance
        of itself.
        """
        self.parser.add_argument(
            self.KEYWORDS_INPUT[0],
            self.KEYWORDS_INPUT[1],
            action='append',
            type=str,
            required=True,
            help='path to annotated variants file (.tsv or .tsv.gz)'
        )
        self.parser.add_argument(
            self.KEYWORDS_MODEL[0],
            self.KEYWORDS_MODEL[1],
            action='append',
            type=str,
            required=True,
            help='path to trained model (.dat)'
        )
        self.parser.add_argument(
            self.KEYWORDS_OUTPUT[0],
            self.KEYWORDS_OUTPUT[1],
            action='append',
            type=str,
            help='path to variant predictions file (.tsv or .tsv.gz)'
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
        input_path = self._validate_file(input_path,
                                         self.ACCEPTED_EXTENSIONS_TSV)

        # Digest model path.
        model_path = self._validate_argument_max_once(self.KEYWORDS_MODEL,
                                                      args.model)
        model_path = self._validate_file(model_path, ('.pickle.dat',))

        # Digest output path.
        output_path = self._validate_argument_max_once(self.KEYWORDS_OUTPUT,
                                                       args.output)
        output_path = self.\
            _generate_path_dynamically(output_path, input_path,
                                       self.ACCEPTED_EXTENSIONS_TSV,
                                       self.ACCEPTED_EXTENSIONS_TSV[1])
        self._validate_force_exists(output_path, args.force)

        # Run predicter.
        print(input_path)
        print(model_path)
        print(output_path)
        # Predicter(input_path, model_path, output_path).predict()
