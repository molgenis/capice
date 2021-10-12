class VerbosityChecker:
    """
    Class to process -v, -vv and -vvv to set the correct loglevel in the logger.
    """
    @staticmethod
    def process_verbosity(info: bool, debug: bool):
        """
        Process the verbosity levels info, debug and trace to return a integer
        corresponding to the Standard Python Library logging Logging levels.
        :param info: bool, the -v flag
        :param debug: bool, the -vv flag
        :return: loglevel, None or int, loglevel corresponding to the input.
        """
        loglevel = None
        if info:
            loglevel = 20
        if debug:
            loglevel = 10
        return loglevel
