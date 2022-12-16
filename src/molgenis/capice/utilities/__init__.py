import functools
import warnings
from pathlib import Path
from collections.abc import Iterable


def get_project_root_dir():
    """
    Function to get the project root directory
    :return: Path instance
    """
    #  This script is within the 5th directory in the project.
    return Path(__file__).parent.parent


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


def check_if_in_list(list_of_lists: list[list[object]], to_check_list: Iterable):
    """
    Checks if the item within a list within a list of object value (can be int, str, float,
    etc.) is within the to_check_list. If False: add to return list. If True: do not add to
    return list.

    Args:
        list_of_lists:
            List containing lists of values (object).
            These values are each independently checked if they are within the to_check_list.
            If False: add to return list. If true: do not add to return list.
        to_check_list:
            Iterable over which the individual items of the list_of_lists should be checked.

    Returns:
        list:
            A single list containing all individual items of list_of_lists that did not occur in
            to_check_list.

    """
    return_list = []
    for items in list_of_lists:
        for item in items:
            if item not in to_check_list:
                return_list.append(item)
    return return_list
