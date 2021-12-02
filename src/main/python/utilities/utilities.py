import functools
import warnings
from pathlib import Path


def get_project_root_dir():
    """
    Function to get the project root directory
    :return: Path instance
    """
    #  This script is within the 5th directory in the project.
    return Path(__file__).parent.parent.parent.parent.parent


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
        raise ValueError('Empty list is given. Should be None or list with elements.')
    elif ls_len > 1:
        raise ValueError('List contains more than 1 item.')
    return ls[0]
