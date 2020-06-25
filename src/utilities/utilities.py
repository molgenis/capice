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


def get_project_root_dir():
    #  This script is 4 directories deep into the project.
    return Path(__file__).parent.parent.parent.parent


def check_file_exists(file_path):
    return os.path.exists(file_path)


def check_dir_exists(path):
    return os.path.isdir(path)


def prepare_dir(path):
    if not check_dir_exists(path):
        os.makedirs(path)


def convert_cla_to_str(cla):
    if isinstance(cla, list):
        return str(cla[0])
    else:
        return cla


def convert_cla_to_int(cla):
    if isinstance(cla, list):
        return int(cla[0])
    else:
        return cla


def convert_cla_to_float(cla):
    if isinstance(cla, list):
        return float(cla[0])
    else:
        return cla
