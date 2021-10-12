import logging
import os
import re

from args_handler_utils import ArgsHandlerUtils
from trainer import Trainer

logger = logging.getLogger(__name__)


class ArgsHandlerTrain:
    """
    Command-line argument handler for train sub-command.
    Parses, validates and executes function.
    """

    def __init__(self, parser):
        self.parser = parser
        self.utils = ArgsHandlerUtils()
        self.parser.set_defaults(func=self._handle_args)

    @classmethod
    def create(cls, parser):
        parser.add_argument(
            '-i',
            '--input',
            nargs=1,
            type=str,
            required=True,
            help='path to classified annotated variants file (.tsv or .tsv.gz)'
        )
        parser.add_argument(
            '-m',
            '--impute',
            nargs=1,
            type=str,
            required=True,
            help='path to impute values file (.json)'
        )
        parser.add_argument(
            '-s',
            '--split',
            nargs=1,
            type=float,
            default=0.2,
            help='proportion of the input data to include '
                 'in the test split (default: %(default)s)'
        )
        parser.add_argument(
            '-o',
            '--output',
            nargs=1,
            type=str,
            help='path to model file (.dat)'
        )
        parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            help='overwrites output if it already exists'
        )

        return cls(parser)

    def _handle_args(self, args):
        self._validate_args(args)

        input_path = os.path.abspath(args.input[0])
        impute_path = os.path.abspath(args.impute[0])
        test_split = args.split[0]

        if args.output:
            output_path = os.path.abspath(args.output[0])
        else:
            output_path = re.sub(r"(\.tsv|\.tsv\.gz)$", "_capice.dat",
                                 input_path)
        self.utils.handle_output_path(self.parser, output_path, args.force)

        Trainer(input_path, impute_path, test_split, output_path).train()

    def _validate_args(self, args):
        input_path = args.input[0]

        if not os.path.exists(input_path):
            self.parser.error(f"input '{input_path}' does not exist")
        if not (input_path.endswith(".tsv") or input_path.endswith(".tsv.gz")):
            self.parser.error(
                f"input '{input_path}' is not a .tsv or .tsv.gz file")
        if not os.path.isfile(input_path):
            self.parser.error(f"input '{input_path}' is not a file")

        impute_path = args.impute[0]
        if not os.path.exists(impute_path):
            self.parser.error(f"impute file '{impute_path}' does not exist")
        if not impute_path.endswith(".json"):
            self.parser.error(
                f"impute file '{impute_path}' is not a .json file")
        if not os.path.isfile(impute_path):
            self.parser.error(f"impute file '{impute_path}' is not a file")

        test_split = args.split[0]
        if test_split < 0 or test_split > 1:
            self.parser.error(
                f"test split '{test_split}' is not between 0 and 1")

        if args.output:
            output_path = args.output[0]
            if not (output_path.endswith(".tsv") or output_path.endswith(
                    ".dat")):
                self.parser.error(f"output '{output_path}' is not a .dat file")
