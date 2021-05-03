from pathlib import Path
import os
import sys
from importlib import import_module


class Printf:
    def __init__(self, verbose: bool):
        self.verbose = verbose

    def printf(self, *args, **kwargs):
        """
        Just like the normal python print,
        but will only print if verbose is set to true.
        :param args: any
        :param kwargs: any print arguments
        """
        if self.verbose:
            print(*args, **kwargs)


def is_gzipped(file_path: str):
    """
    Function to check if the given file path is gzipped
    :param file_path: str
    :return: bool
    """
    return file_path.endswith('.gz')


def get_project_root_dir():
    """
    Function to get the project root directory
    :return: Path instance
    """
    #  This script is 4 directories deep into the project.
    return Path(__file__).parent.parent.parent.parent.parent.parent


def check_file_exists(file_path: str):
    """
    Function to check if a file exists
    :param file_path: str
    :return: bool
    """
    return os.path.exists(file_path)


def check_dir_exists(path: str):
    """
    Function to check if a path exists
    :param path: str
    :return: bool
    """
    return os.path.isdir(path)


def prepare_dir(path: str):
    """
    Function to make a path if does not exist
    :param path: str
    """
    if not check_dir_exists(path):
        os.makedirs(path)


def convert_cla_to_str(cla: any):
    """
    Function to convert a Command Line Argument to string.
    Will return the given argument if not a list.
    :param cla: any
    :return: any
    """
    if isinstance(cla, list):
        return str(cla[0])
    else:
        return cla


def convert_cla_to_int(cla: any):
    """
    Function to convert a Command Line Argument to integer.
    Will return the given argument if not a list.
    :param cla: any
    :return: any
    """
    if isinstance(cla, list):
        return int(cla[0])
    else:
        return cla


def convert_cla_to_float(cla: any):
    """
    Function to convert a Command Line Argument to float.
    Will return the given argument if not a list.
    :param cla: any
    :return: any
    """
    if isinstance(cla, list):
        return float(cla[0])
    else:
        return cla


def convert_cla_to_full_string(cla: any):
    """
    Function to convert large multiple words arguments to a single string.
    Will return the given argument if not a list.
    :param cla: any
    :return: str or None
    """
    if isinstance(cla, list):
        return " ".join(cla)
    else:
        return cla


def load_modules(path):
    """
    Utilities function to dynamically load in modules in the given path
    :param path: path to the modules
    :return: list
    """
    modules = []
    for module in os.listdir(path):
        if module.endswith('.py'):
            if not module.endswith('__.py') and not module.endswith('abstract.py'):
                modules.append(module)
    return modules


def importer(usable_modules: list, path):
    """
    Utilitarian function for the imputer and preprocessor to dynamically load in the modules using the import_module
    library.
    :param usable_modules: list of modules present within a certain directory
    :param path: path of said directory
    :return: list of usable modules
    """
    return_modules = []
    sys.path.append(path)
    for module in usable_modules:
        module = module.split('.py')[0]
        imported_module = import_module(module)
        return_modules.append(_importer(imported_module=imported_module))
    sys.path.remove(path)
    return return_modules


def _importer(imported_module):
    for attribute in dir(imported_module):
        if not attribute.startswith('Template') and not attribute.startswith('__'):
            get_attribute = getattr(imported_module, attribute)
            if 'name' in dir(get_attribute) and 'usable' in dir(get_attribute):
                if get_attribute().usable is True:
                    return get_attribute()


def get_filename_and_extension(path):
    """
    Function to get the filename and extension of a file from a given input path or input filename.
    :param path: string
    :return: filename (string), extension (string)
    """
    no_path = os.path.basename(path)
    splitted_path = no_path.split('.')
    filename = splitted_path[0]
    extension = ".".join(splitted_path[1:])
    return filename, extension
