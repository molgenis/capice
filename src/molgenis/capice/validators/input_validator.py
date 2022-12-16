import os
import warnings
from pathlib import Path


class InputValidator:
    """
    Validator for the CLI arguments
    """
    @staticmethod
    def validate_input_path(input_path: os.PathLike, extension: tuple[str]):
        """
        Function to validate if there is a file at the input location
        :param input_path: full path to input file
        :param extension: string of what the input file should end with.
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f'{input_path} does not exist!')
        if not str(input_path).endswith(extension):
            raise IOError(f'{input_path} does not match required extension: '
                          f'{", ".join(extension)}')

    @staticmethod
    def validate_output_path(output_path):
        """
        Function to validate if the output directory exists and,
        if not, make it.
        :param output_path: path to output folder
        """
        # If the output directory is not present and
        # the parent directory is also not writeable, throw OSError
        if not os.path.isdir(output_path) and not os.access(Path(output_path).parent, os.W_OK):
            raise OSError('New output directory cannot be made in a read/execute only directory!')
        # If the output directory is present but not writable, throw OSError
        elif os.path.isdir(output_path) and not os.access(output_path, os.W_OK):
            raise OSError('Output directory is not writable!')
        # If the output directory is not yet present,
        # but passed the check that it is in a writable parent directory,
        # only warn
        elif not os.path.isdir(output_path):
            warnings.warn("Output directory does not exist, creating.")
            os.makedirs(output_path)
        # No else is required, since the else would be to place the output file
        # in a writeable output directory that is already present.
