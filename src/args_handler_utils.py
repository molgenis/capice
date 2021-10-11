import logging
import os

logger = logging.getLogger(__name__)


class ArgsHandlerUtils:
    @staticmethod
    def validate_input_tsv(parser, input_path):
        if not os.path.exists(input_path):
            parser.error(f"input '{input_path}' does not exist.")
        if not (input_path.endswith(".tsv") or input_path.endswith(".tsv.gz")):
            parser.error(f"input '{input_path}' is not a .tsv or .tsv.gz file.")
        if not os.path.isfile(input_path):
            parser.error(f"input '{input_path}' is not a file.")

    @staticmethod
    def handle_output_path(parser, output_path, force):
        if os.path.exists(output_path):
            if not force:
                parser.error(f"output '{output_path}' already exist, use -f/--force to overwrite.")
            elif not os.path.isfile(output_path):
                parser.error(f"output '{output_path}' is not a file.")
            else:
                logger.info("removing existing output '%s'", output_path)
                os.remove(output_path)

