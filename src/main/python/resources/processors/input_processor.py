import os
from src.main.python.resources.utilities.utilities import \
    get_filename_and_extension


class InputProcessor:
    def __init__(self, call_dir, input_path, output_path, force):
        """
        InputProcessor checks the input directory, output directory
        (being either call_dir if output_path is None or output_path) and
        the force flag to build the output directory and output filename.
        :param input_path: str, path-like
        :param output_path: str, path-like (if missing: supply None)
        :param force: bool, force flag present or not

        Use getter get_output_filename() to get the output filename after
        initialization and get_output_directory() to get the output directory.
        (output directory is not yet checked for write-ability and existence)
        """
        self.call_dir = call_dir
        self.input_path = input_path
        self.output_path = output_path
        self.force = force
        self.output_directory = ''
        self.output_filename = ''
        self._handle_input_output_directories()

    def _handle_input_output_directories(self):
        """
        Function to validate the input location, output location and filename to
        tell the exporter where to place what file.
        """
        if self.output_path is None:
            self._create_capice_output_filename(input_path=self.input_path,
                                                export_to_call=True)
        else:
            # Check if it is a path or else just a filename
            if len(os.path.dirname(self.output_path)) > 0:
                # Then I know it's an output filepath + possibly name
                if os.path.splitext(self.output_path)[1] != '':
                    # Then I know it is a full path + filename
                    self._create_capice_output_filename(
                        input_path=self.output_path,
                        append_capice=False)
                else:
                    # Then I know it's a full path
                    self._create_capice_output_filename(
                        input_path=self.input_path,
                        output_path=self.output_path,
                        ispath=True)
            else:
                # Then I know it's an output filename
                self.output_directory = self.call_dir
                self.output_filename = self.output_path

        self._check_force()

    def _check_force(self):
        full_ouput_path = os.path.join(self.output_directory,
                                       self.output_filename)
        if not self.force and os.path.isfile(full_ouput_path):
            raise FileExistsError(
                f'Output file {full_ouput_path} already exists! '
                f'Use -f / --force to overwrite.')

    def _create_capice_output_filename(self, input_path, output_path=None,
                                       append_capice=True, ispath=False,
                                       export_to_call=False):
        """
        Input path = absolute path of the input file, including filename itself.
        Can also be the output path, but then a full output path including
        filename.
        output path = absolute path to the output, if None the input path will
        be used to output.
        append_capice: whenever '<filename>_capice.<extension> should be added.
        ispath: Whenever the output path is a sole path and does not contain a
        filename
        export_to_call: True when output is None.
        """
        if output_path is None and not export_to_call:
            output_path = input_path
        elif output_path is None and export_to_call:
            output_path = self.call_dir
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

    def get_output_filename(self):
        return self.output_filename

    def get_output_directory(self):
        return self.output_directory
