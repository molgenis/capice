import functools
import warnings
from pathlib import Path


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
