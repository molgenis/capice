from src.utilities.utilities import check_file_exists
from src.logger import Logger
import os


class Exporter:
    """
    Singleton class used to export the files produced by CAPICE.
    """
    class __Exporter:
        def __init__(self):
            self.force = False
            self.log = Logger().get_logger()

        def set_force(self, force):
            self.force = force

        def get_force(self):
            return self.force

        def export_filename_ready(self, file_path, file_name: str, extension: str):
            overwrite = self.force
            path_and_filename = os.path.join(file_path, file_name)
            full_path = os.path.join(file_path, file_name + extension)
            export_path = None
            if not check_file_exists(full_path):
                self.log.info('No file found at {}, save to create.'.format(full_path))
                export_path = full_path
            elif overwrite and check_file_exists(full_path):
                self.log.info('Found existing file at {}, removing file for overwriting.'.format(full_path))
                os.remove(full_path)
                export_path = full_path
            else:
                self.log.info('Found existing file at {}, not able to overwrite. Creating new filename.'.format(
                    full_path
                ))
                export_exists = True
                extension_counter = 1
                while export_exists:
                    attempted_file = path_and_filename + "_{}".format(extension_counter) + extension
                    if not check_file_exists(attempted_file):
                        self.log.info('Able to create {}'.format(attempted_file))
                        export_exists = False
                        export_path = attempted_file
                    extension_counter += 1
            return export_path

    instance = None

    def set_force(self, force):
        """
        Function to set the global output Force command
        :param force: bool
        """
        pass

    def get_force(self):
        """
        Function to get the global output Force command
        :return: bool
        """
        pass

    def export_filename_ready(self, file_path, file_name, extension: str):
        """
        Function to prepare a file to be exported utilizing the Force command
        :param file_path: path-like, path to where the file should be put
        :param file_name: str: name of the file without the extension
        :param extension: str: extension of the file (for example .tsv.gz for a gzipped tab separated file)
        :return: path-like, full path of the new file
        """
        pass

    def __new__(cls):
        """
        Class method to set export instance
        :return: instance
        """
        if not Exporter.instance:
            Exporter.instance = Exporter.__Exporter()
        return Exporter.instance

    def __init__(self):
        """
        __init__ method to set instance to Exporter.__Exporter()
        """
        if not Exporter.instance:
            Exporter.instance = Exporter.__Exporter()

    def __getattr__(self, name):
        """
        Method to return the value of the named attribute of name
        :param name: str
        :return: str
        """
        return getattr(self.instance, name)


def create_log_export_name(file_path, file_name):
    """
    Function to create the log file name
    :param file_path: path-like, path to put the log file in
    :param file_name: str, name of the logfile
    :return: path-like, full path of the exporting log file
    """
    full_export = os.path.join(file_path, file_name + '.log')
    partial_export = os.path.join(file_path, file_name)
    export_path = None
    if check_file_exists(full_export):
        log_file_exist = True
        counter = 1
        while log_file_exist:
            attempted_filename = partial_export + '_{}.log'.format(counter)
            if not check_file_exists(attempted_filename):
                log_file_exist = False
                export_path = attempted_filename
            counter += 1
    else:
        export_path = full_export
    return export_path
