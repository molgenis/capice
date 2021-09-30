from pathlib import Path
import os
import sys
from importlib import util
import warnings
import functools
import logging


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


def load_modules(path):
    """
    Utilities function to dynamically load in modules in the given path
    :param path: path to the modules
    :return: list
    """
    modules = []
    for module in os.listdir(path):
        if module.endswith('.py') and \
                not module.endswith('__.py') and \
                not module.endswith('abstract.py'):
            modules.append(module)
    return modules


def importer(usable_modules: list):
    """
    Utilitarian function for the imputer and preprocessor to dynamically load
    in the modules using the import_module library.
    :param usable_modules: list of absolute paths to potential modules
    :return: list of usable modules
    """
    return_modules = []
    for module in usable_modules:
        name = os.path.basename(module).split('.py')[0]
        spec = util.spec_from_file_location(
            name=name,
            location=module
        )
        loaded_module = _process_spec(spec)
        if loaded_module:
            return_modules.append(loaded_module)
    return return_modules


def _process_spec(spec):
    return_spec = None
    loaded_spec = util.module_from_spec(spec)
    spec.loader.exec_module(loaded_spec)
    for attribute in dir(loaded_spec):
        if not attribute.startswith('Template') and \
                not attribute.startswith('__'):
            get_attribute = getattr(loaded_spec, attribute)
            if 'name' in dir(get_attribute) and \
                    'usable' in dir(get_attribute) and \
                    get_attribute().usable is True:
                return_spec = get_attribute()
    return return_spec


def get_filename_and_extension(path):
    """
    Function to get the filename and extension of a file from a given input
    path or input filename.
    :param path: string
    :return: filename (string), extension (string)
    """
    no_path = os.path.basename(path)
    splitted_path = no_path.split('.')
    filename = splitted_path[0]
    extension = ".".join(splitted_path[1:])
    return filename, extension


def deprecated(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)
        warnings.warn('Call to deprecated function {}.'.format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)
        return func(*args, **kwargs)
    return new_func


class SetCustomLoggingFilter(logging.Filter):
    def __init__(self, custom_loglevels):
        super(SetCustomLoggingFilter, self).__init__()
        self.custom_loglevels = custom_loglevels

    def filter(self, record) -> bool:
        return record.levelno in self.custom_loglevels
