import os
import logging
import warnings
import functools
from pathlib import Path
from importlib import util


def get_project_root_dir():
    """
    Function to get the project root directory
    :return: Path instance
    """
    #  This script is 5 directories deep into the project.
    return Path(__file__).parent.parent.parent.parent.parent


def load_modules(path):
    """
    Utilities function to dynamically load in modules in the given path
    :param path: path to the modules
    :return: list
    """
    modules = []
    for module in os.listdir(path):
        module = os.path.join(path, module)
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
    return_modules = {}
    for module in usable_modules:
        name = os.path.basename(module).split('.py')[0]
        spec = util.spec_from_file_location(
            name=name,
            location=module
        )
        loaded_module = _process_spec(spec)
        if loaded_module and module not in return_modules.keys():
            return_modules[module] = loaded_module
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
    """
    Custom logging filter class to make sure that stdout only contains
    INFO or DEBUG calls.
    """
    def __init__(self, custom_loglevels):
        """
        :param custom_loglevels: str or iterable: the loglevels that should pass
        this logging filter.
        """
        super(SetCustomLoggingFilter, self).__init__()
        self.custom_loglevels = custom_loglevels

    def filter(self, record) -> bool:
        return record.levelno in self.custom_loglevels


def validate_list_length_one(ls):
    """
    Validates whether ls contains only 1 argument. If None, it simply
    returns None. If a list is given, validates whether it contains only
    1 element. If it is an empty list or contains more than 1 element,
    throws a ValueError.
    :param list[str] ls: the list to be validated
    :return: None or the first item from the given list
    :raise ValueError: if list with 0 or more than 1 elements is given
    """
    if ls is None:
        return ls

    ls_len = len(ls)
    if ls_len == 0:
        raise ValueError('Empty list is given. Should be None or list with '
                         'elements.')
    elif ls_len > 1:
        raise ValueError('List contains more than 1 item.')
    return ls[0]
