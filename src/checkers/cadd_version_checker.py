from src.logger import Logger
import warnings

# Note for later: call with if not None in arguments


class CaddVersionChecker:
    """
    Class to check the given CADD command line arguments and the header of the CADD file
    """
    def __init__(self,
                 cla_cadd_version: float,
                 cla_grch_build: int,
                 file_cadd_version: float,
                 file_grch_build: int):
        """
        Class to check the given CADD command line arguments and the header of the CADD file
        :param cla_cadd_version: float, command line argument for the used CADD version
        :param cla_grch_build: int, command line argument for the used GRCh build
        :param file_cadd_version: float, the CADD version present in the header of the CADD file
        :param file_grch_build: int, the GRCh build present in the header of the CADD file
        """
        self.cla_cadd_version = cla_cadd_version
        self.cla_grch_build = cla_grch_build
        self.file_cadd_version = file_cadd_version
        self.file_grch_build = file_grch_build
        self.log = Logger().get_logger()
        self.export_cadd_version = None
        self.export_grch_build = None

    def _check_version_match(self):
        if self.cla_cadd_version != self.file_cadd_version:
            warning_message = "Version supplied on the command line:" \
                              " {} does not match the CADD file version: {}!".format(
                                self.cla_cadd_version,
                                self.file_cadd_version
                                )
            warnings.warn(warning_message)
            self.log.warning(warning_message)
        else:
            self.log.info('CADD versions from the command line and file match.')
        self.export_cadd_version = self.file_cadd_version

    def _check_grch_build_match(self):
        if self.cla_grch_build != self.file_grch_build:
            warning_message = "GRCh build supplied on the command line:" \
                              " {} does not match the CADD file GRCh build: {}!".format(
                                self.cla_cadd_version,
                                self.file_cadd_version
                                )
            warnings.warn(warning_message)
            self.log.warning(warning_message)
        else:
            self.log.info('GRCh builds from the command line and file match.')
        self.export_grch_build = self.file_grch_build

    def check(self):
        """
        Function to call the check of the GRCh build and CADD version
        :return: cadd_version: float, grch_build: int
        """
        self._check_version_match()
        self._check_grch_build_match()
        return self.export_cadd_version, self.export_grch_build
