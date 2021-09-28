from src.main.python.resources.errors.errors import InputError
from src.main.python.resources.utilities.utilities import prepare_dir,\
    check_dir_exists, check_file_exists, get_filename_and_extension
import warnings
import os
from pathlib import Path


class InputChecker:
    """
    Checker for the remaining supplied arguments
    """

    def __init__(self):
        self.output_filename = ''
        self.output_directory = ''
        self._call_loc = str(Path('.').absolute())

    @staticmethod
    def check_input_loc(input_loc):
        """
        Function to check if there is a file at the input location
        :param input_loc: full path to input file
        """
        if not check_file_exists(input_loc):
            raise InputError("Input file does not exist!")
        return input_loc

    @staticmethod
    def check_output_loc(output_loc):
        """
        Function to check if the output directory exists and, if not, make it.
        :param output_loc: path to output folder
        """
        if not check_dir_exists(output_loc):
            warnings.warn("Output directory does not exist, creating.")
            prepare_dir(output_loc)

    def check_input_output_directories(self, input_path, output_path, force):
        """
        Function to check the input location, output location and filename to
        tell the exporter where to place what file.
        :param input_path: str, path-like
        :param output_path: str, path-like (if missing: supply None)
        """
        if output_path is None:
            self._create_capice_output_filename(input_path=input_path,
                                                export_to_call=True)
        else:
            # Check if it is a path or else just a filename
            if len(os.path.dirname(output_path)) > 0:
                # Then I know it's an output filepath + possibly name
                if os.path.splitext(output_path)[1] != '':
                    # Then I know it is a full path + filename
                    self._create_capice_output_filename(input_path=output_path,
                                                        append_capice=False)
                else:
                    # Then I know it's a full path
                    self._create_capice_output_filename(input_path=input_path,
                                                        output_path=output_path,
                                                        ispath=True)
            else:
                # Then I know it's an output filename
                self.output_directory = self._call_loc
                self.output_filename = output_path
        self._check_gzip_extension()
        self._check_force(force)

    def _check_force(self, force):
        full_ouput_path = os.path.join(self.output_directory,
                                       self.output_filename)
        if not force and os.path.isfile(full_ouput_path):
            raise FileExistsError(
                f'Output file {full_ouput_path} already exists! '
                f'Use -f / --force to overwrite.')

    def _create_capice_output_filename(self, input_path, output_path=None,
                                       append_capice=True, ispath=False,
                                       export_to_call=False):
        if output_path is None and not export_to_call:
            output_path = input_path
        elif output_path is None and export_to_call:
            output_path = self._call_loc
            ispath = True
        input_filename, extension = get_filename_and_extension(input_path)
        if append_capice:
            self.output_filename = '{}_capice.{}'.format(input_filename,
                                                         extension)
        else:
            self.output_filename = '{}.{}'.format(input_filename, extension)
        if ispath:
            self.output_directory = output_path
        else:
            self.output_directory = os.path.dirname(output_path)

    def _check_gzip_extension(self):
        if not self.output_filename.endswith('.gz'):
            self.output_filename = self.output_filename + '.gz'

    @staticmethod
    def check_reference(reference):
        """
        Function to check if the reference files exist
        """
        locs = [reference, f'{reference}.fai']
        for loc in locs:
            if loc is False or not check_file_exists(loc):
                raise FileNotFoundError(
                    'Unable to locate all required files to annotate.'
                )

    def get_output_filename(self):
        return self.output_filename

    def get_output_directory(self):
        return self.output_directory
