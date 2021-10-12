from src.predicter import Predicter
from src.main.python.core.global_manager import CapiceManager
from src.main.python.resources.Validators import InputValidator


class ArgsHandlerPredict:
    """
    Command-line argument handler for predict sub-command.
    Parses, validates and executes function.
    """

    def __init__(self, parser):
        self.parser = parser
        self.validator = InputValidator()
        self.manager = CapiceManager()

    def create(self):
        """
        Classmethod create for ArgsHandlerPredict, to create arguments specific
        to the Predict module of CAPICE. Will return an initialized instance
        of itself.
        """
        self.parser.add_argument(
            '-i',
            '--input',
            nargs=1,
            type=str,
            required=True,
            help='path to annotated variants file (.tsv or .tsv.gz)'
        )
        self.parser.add_argument(
            '-m',
            '--model',
            nargs=1,
            type=str,
            required=True,
            help='path to trained model (.dat)'
        )
        self.parser.add_argument(
            '-o',
            '--output',
            nargs=1,
            type=str,
            help='path to variant predictions file (.tsv or .tsv.gz)'
        )
        self.parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            help='overwrites output if it already exists'
        )

    def handle(self):
        self.parser.set_defaults(func=self._handle_args)

    def _handle_args(self, args):
        input_path = args.input[0]
        model_path = args.model[0]
        output_path = args.output
        if args.output is not None:
            output_path = args.output[0]
            self.validator.validate_output_loc(output_path)

        self.validator.validate_input_loc(input_path)
        self.validator.validate_input_output_directories(
            input_path=input_path,
            output_path=output_path,
            force=args.force
        )
        validated_output_path = self.validator.get_output_directory()
        self.manager.output_filename = self.validator.get_output_filename()

        Predicter(input_path, model_path, validated_output_path).predict()
