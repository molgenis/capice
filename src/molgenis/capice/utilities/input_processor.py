import os
from pathlib import Path


class InputProcessor:
    def __init__(self, input_path, output_path, force, default_extension):
        """
        InputProcessor checks the input directory, output directory
        (being either call_dir if output_path is None or output_path) and
        the force flag to build the output directory and output filename.
        :param input_path: str, path-like
        :param output_path: str, path-like (if missing: supply None)
        :param force: bool, force flag present or not
        :param default_extension: str, the default extension the output file should get in case
        output is missing from CLI

        Use getter get_output_filename() to get the output filename after
        initialization and get_output_directory() to get the output directory.
        (output directory is not yet checked for writability and existence)

        Note: when only the input_path is provided or only a file directory is
        supplied, InputProcessor will strip the extension from the input path
        and use the the input path file name as reference for the output
        filename. (so input with example.tsv.gz will be come example).
        Extension has to be manually added within the argument parser.
        """
        self.call_dir = str(Path('.').absolute())
        self.input_path = input_path
        self.output_path = output_path
        self.output_given = False
        self.force = force
        self.default_extension = default_extension
        self.output_directory = ''
        self.output_filename = ''
        self._handle_input_output_directories()

    def _handle_input_output_directories(self):
        """
        Function to validate the input location, output location and filename to
        tell the exporter where to place what file.
        """
        if self.output_path is None:
            filename = self.get_filename_from_path(self.input_path)
            self._set_output_path(self.call_dir, filename)
        else:
            # Check if it is a path or else just a filename
            if len(os.path.dirname(self.output_path)) > 0 or self.output_path == '.':
                # Then I know it's an output filepath + possibly name
                if os.path.splitext(self.output_path)[1] != '':
                    # Then I know it is a full path + filename
                    self._set_output_path(os.path.dirname(self.output_path),
                                          os.path.basename(self.output_path))
                    self.output_given = True
                else:
                    # Then I know it's a full path
                    filename = self.get_filename_from_path(self.input_path)
                    self._set_output_path(self.output_path, filename)
            else:
                # Then I know it's an output filename
                self._set_output_path(self.call_dir, self.output_path)

        self._check_force()

    def _check_force(self):
        full_output_path = os.path.join(self.output_directory, self.output_filename)
        if not self.force and os.path.isfile(full_output_path):
            raise FileExistsError(
                f'Output file {full_output_path} already exists! Use -f / --force to overwrite.')

    def _set_output_path(self, directory, filename):
        self.output_directory = directory
        self.output_filename = filename

    def get_filename_from_path(self, path):
        """
        Function to get the filename of a file from a given input
        path or input filename.
        :param path: string
        :return: filename (string)
        """
        no_path = os.path.basename(path)
        splitted_path = no_path.split('.')
        filename = splitted_path[0]
        return f'{filename}_capice{self.default_extension}'

    def get_output_filename(self):
        return self.output_filename

    def get_output_directory(self):
        return self.output_directory

    def get_output_given(self):
        return self.output_given
