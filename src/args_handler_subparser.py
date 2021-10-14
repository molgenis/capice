import os
import warnings
from abc import ABCMeta, abstractmethod
from os import makedirs
from os.path import basename, isdir, abspath, isfile, exists, dirname
from pathlib import Path


class ArgsHandlerSubparser(metaclass=ABCMeta):
    _call_loc = str(Path('.').absolute())

    def __init__(self, parser):
        self.parser = parser

    @abstractmethod
    def create(self):
        pass

    def handle(self):
        self.parser.set_defaults(func=self._handle_args)

    @abstractmethod
    def _handle_args(self):
        pass

    def _validate_argument_max_once(self, keywords, parsed_arg):
        """
        Validates whether parsed_arg contains only 1 argument. If None, this
        indicates an non-filled optional argument which is allowed (and simply
        returns None). If a list is given, validates whether it contains only
        1 element (if 0 raises exception, if more throws `parser.error()`)
        :param tuple[str] keywords: keywords belonging to parsed_arg
        :param list[str] parsed_arg: the list which should be validated
        :return: None or the first item from the given list
        :raise ValueError: if empty list is given
        """
        if parsed_arg is None:
            return parsed_arg

        parsed_arg_len = len(parsed_arg)
        if parsed_arg_len == 0:
            raise ValueError('Empty list is given. Should be None or list '
                             'with elements.')
        elif parsed_arg_len == 1:
            return parsed_arg[0]
        self.parser.error(f'{" / ".join(keywords)} was found more than once!')

    def _validate_dir(self, dir_path, must_exist=True):
        dir_path = abspath(dir_path)
        if not isdir(dir_path):
            if must_exist:
                self.parser.error(f'{dir_path} does not exist')
            else:
                warnings.warn('Output directory does not exist, creating.')
                makedirs(dir_path)
        # Return absolute path.
        return dir_path

    def _validate_file(self, file_path, accepted_extensions,
                       is_readable=True):
        file_path = abspath(file_path)
        # Validates if file_path is existing readable file if needed.
        if is_readable:
            if not isfile(file_path) or not os.access(file_path, os.R_OK):
                self.parser.error(f'{file_path} is not a readable file')

        # Validates file extension.
        extension = '.' + '.'.join(basename(file_path).split('.')[1:])
        if extension not in accepted_extensions:
            self.parser.error(f'{file_path} contains an invalid extension. '
                              f'Accepted extensions: {accepted_extensions}')
        # Returns absolute path.
        return file_path

    def _validate_force_exists(self, file_path, force_arg):
        if not force_arg and exists(file_path):
            self.parser.error(f'Output file {file_path} already exists! '
                              f'Use -f / --force to overwrite.')

    def _validate_range(self, keyword, value, range):
        accepted_types = (int, float)
        if type(value) not in accepted_types:
            raise ValueError(f'{value} should be of type {accepted_types}')

        if value < range[0] or value > range[1]:
            self.parser.error(
                f'{keyword}: {value} should be between {range[0]} and '
                f'{range[1]} (inclusive)')

        return value

    @staticmethod
    def _generate_filename(reference_file_path, new_extension, postfix=''):
        return basename(reference_file_path).split('.')[0] + postfix + \
               new_extension

    @staticmethod
    def _generate_basic_path(filename, directory=_call_loc):
        return directory.rstrip('/') + '/' + filename

    def _generate_path_dynamically(self, path, reference_path,
                                   accepted_file_extensions,
                                   default_extension,
                                   default_postfix='_capice'):
        # Default filename to use.
        default_filename = self._generate_filename(reference_path,
                                        default_extension,
                                        postfix=default_postfix)

        # Use default filename in call dir if no path is given.
        if path is None:
            path = self._generate_basic_path(default_filename)
        # Validate/generate directories (preferably should be done later).
        self._validate_dir(dirname(path), must_exist=False)
        # If path is a directory, use default filename.
        if isdir(path):
            path = self._generate_basic_path(default_filename, directory=path)
        # Validate and return file path.
        return self._validate_file(path, accepted_file_extensions,
                                   is_readable=False)
