import logging
import os
import re

from src.args_handler_utils import ArgsHandlerUtils
from src.predicter import Predicter

logger = logging.getLogger(__name__)


class ArgsHandlerPredict:
    """
    Command-line argument handler for predict sub-command.
    Parses, validates and executes function.
    """

    def __init__(self, parser):
        self.parser = parser
        self.parser.set_defaults(func=self.__handle_args)

    @staticmethod
    def create(parser):
        parser.add_argument('-i',
                            '--input',
                            nargs=1,
                            type=str,
                            required=True,
                            help='path to annotated variants file (.tsv or .tsv.gz)')
        parser.add_argument('-m',
                            '--model',
                            nargs=1,
                            type=str,
                            required=True,
                            help='path to trained model (.dat)')
        parser.add_argument('-o',
                            '--output',
                            nargs=1,
                            type=str,
                            help='path to variant predictions file (.tsv or .tsv.gz)')
        parser.add_argument('-f',
                            '--force',
                            action='store_true',
                            help='overwrites output if it already exists')
        return ArgsHandlerPredict(parser)

    def __handle_args(self, args):
        self.__validate_args(args)

        input_path = os.path.abspath(args.input[0])
        model_path = os.path.abspath(args.model[0])

        if args.output:
            output_path = os.path.abspath(args.output[0])
        else:
            output_path = re.sub(r"(\.tsv|\.tsv\.gz)$", "_capice.tsv.gz", input_path)
        ArgsHandlerUtils.handle_output_path(self.parser, output_path, args.force)

        Predicter(input_path, model_path, output_path).predict()

    def __validate_args(self, args):
        ArgsHandlerUtils.validate_input_tsv(self.parser, args.input[0])

        if args.output:
            output_path = args.output[0]
            if not (output_path.endswith(".tsv") or output_path.endswith(".tsv.gz")):
                self.parser.error(f"output '{output_path}' is not a .tsv or .tsv.gz file.")
