from pathlib import Path
import os


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
    return Path(__file__).parent.parent.parent.parent


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
