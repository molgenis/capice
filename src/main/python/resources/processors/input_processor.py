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

        Note: when only the input_path is provided or only a file directory is
        supplied, InputProcessor will strip the extension from the input path
        and use the the input path file name as reference for the output
        filename. (so input with example.tsv.gz will be come example).
        Extension has to be manually added within the argument parser.
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
            self._build_output_from_input()
        else:
            # Check if it is a path or else just a filename
            if len(os.path.dirname(self.output_path)) > 0:
                # Then I know it's an output filepath + possibly name
                if os.path.splitext(self.output_path)[1] != '':
                    # Then I know it is a full path + filename
                    self._build_output_from_output_directory_and_filename()
                else:
                    # Then I know it's a full path
                    self._build_output_from_output_directory()
            else:
                # Then I know it's an output filename
                self._build_output_from_output_filename()

        self._check_force()

    def _check_force(self):
        full_ouput_path = os.path.join(self.output_directory,
                                       self.output_filename)
        if not self.force and os.path.isfile(full_ouput_path):
            raise FileExistsError(
                f'Output file {full_ouput_path} already exists! '
                f'Use -f / --force to overwrite.')

    def _build_output_from_input(self):
        """
        Method to build an output directory and output filename from the input.
        Reset of extension is required, since in train, the extension is set
        from a TSV input to a pickle.dat output.
        """
        self.output_directory = self.call_dir
        fn = get_filename_and_extension(self.input_path)[0]
        self.output_filename = f'{fn}_capice'

    def _build_output_from_output_filename(self):
        """
        Method to build the output directory and output filename from
        the output argument being just a file name, but the output directory
        is set to the call location.
        """
        self.output_directory = self.call_dir
        self.output_filename = self.output_path

    def _build_output_from_output_directory(self):
        """
        Method to build an output directory and output filename from the user
        provided output directory and the input filename. Reset of input
        filename extension is required for train.
        """
        self.output_directory = self.output_path
        fn = get_filename_and_extension(self.input_path)[0]
        self.output_filename = f'{fn}_capice'

    def _build_output_from_output_directory_and_filename(self):
        """
        Method to build the output directory and filename from user provided
        output argument.
        """
        self.output_directory = os.path.dirname(self.output_path)
        self.output_filename = os.path.basename(self.output_path)

    def get_output_filename(self):
        return self.output_filename

    def get_output_directory(self):
        return self.output_directory
