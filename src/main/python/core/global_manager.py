from src.main.python.resources.checkers.property_checker import PropertyChecker


class CapiceManager:
    """
    Test
    """
    class __CapiceManager:
        """
        Class to make a logfile on the progress being made.
        """
        def __init__(self):
            self.property_checker = PropertyChecker()
            self.log_loc = '.'
            self.now = None
            self.overwrite_impute = False
            self.overwrite_model = False
            self.cadd_version = 0.0
            self.grch_build = 0
            self.force = False
            self.verbose = False
            self.enable_logfile = False
            self.critical_logging_only = False
            self.cadd_features = []
            self.output_filename = ''

        @property
        def log_loc(self):
            return self._log_loc

        @log_loc.setter
        def log_loc(self, value):
            self.property_checker.check_property(value=value, expected_type=str)
            self._log_loc = value

        @property
        def now(self):
            return self._now

        @now.setter
        def now(self, value):
            self._now = value

        @property
        def overwrite_impute(self):
            return self._overwrite_impute

        @overwrite_impute.setter
        def overwrite_impute(self, value=None):
            self.property_checker.check_property(value=value, expected_type=(str, bool))
            self._overwrite_impute = value

        @property
        def overwrite_model(self):
            return self._overwrite_model

        @overwrite_model.setter
        def overwrite_model(self, value):
            self.property_checker.check_property(value=value, expected_type=(str, bool))
            self._overwrite_model = value

        @property
        def cadd_version(self):
            return self._cadd_version

        @cadd_version.setter
        def cadd_version(self, value):
            self.property_checker.check_property(value=value, expected_type=float, include_none=True)
            self._cadd_version = value

        @property
        def grch_build(self):
            return self._grch_build

        @grch_build.setter
        def grch_build(self, value):
            self.property_checker.check_property(value=value, expected_type=int, include_none=True)
            self._grch_build = value

        @property
        def cadd_features(self):
            return self._cadd_features

        @cadd_features.setter
        def cadd_features(self, value):
            self.property_checker.check_property(value=value, expected_type=list)
            self._cadd_features = value

        @property
        def force(self):
            return self._force

        @force.setter
        def force(self, value):
            self.property_checker.check_property(value=value, expected_type=bool)
            self._force = value

        @property
        def verbose(self):
            return self._verbose

        @verbose.setter
        def verbose(self, value):
            self.property_checker.check_property(value=value, expected_type=bool)
            self._verbose = value

        @property
        def enable_logfile(self):
            return self._enable_logfile

        @enable_logfile.setter
        def enable_logfile(self, value):
            self.property_checker.check_property(value=value, expected_type=bool)
            self._enable_logfile = value

        @property
        def critical_logging_only(self):
            return self._critical_logging_only

        @critical_logging_only.setter
        def critical_logging_only(self, value):
            self.property_checker.check_property(value=value, expected_type=bool)
            self._critical_logging_only = value

        @property
        def output_filename(self):
            return self._output_filename

        @output_filename.setter
        def output_filename(self, value):
            self.property_checker.check_property(value=value, expected_type=str)
            self._output_filename = value

    instance = None

    @property
    def log_loc(self):
        """
        Getter for setter log_loc

        :return: string
        """
        return self._log_loc

    @log_loc.setter
    def log_loc(self, value):
        """
        Singleton property log_loc, to set the location of the logfile.

        :param value: string
        """
        pass

    @property
    def now(self):
        """
        Getter for setter now

        :return: datetime instance
        """
        return self._now

    @now.setter
    def now(self, value):
        """
        Singleton property now, to set a datetime instance of when program instance started.

        :param value: datetime instance
        """
        pass

    @property
    def overwrite_impute(self):
        """
        Getter for setter overwrite_impute

        :return: False or string
        """
        return self._overwrite_impute

    @overwrite_impute.setter
    def overwrite_impute(self, value=None):
        """
        Singleton property overwrite_impute, to set a string for the imputer to overwrite the CADD version and genome
        build. Raises a TypeError if not supplied with a string or False.

        :param value: False or string
        """
        pass

    @property
    def overwrite_model(self):
        """
        Getter for setter overwrite_model

        :return: False or string
        """
        return self._overwrite_model

    @overwrite_model.setter
    def overwrite_model(self, value):
        """
        Singleton property overwrite_model, to set a string for the preprocessor and predictor to overwrite the
        CADD version and genome build. Raises a TypeError if not supplied with a string or False.

        :param value: False or string
        """
        pass

    @property
    def cadd_version(self):
        """
        Getter for setter cadd_version

        :return: float
        """
        return self._cadd_version

    @cadd_version.setter
    def cadd_version(self, value):
        """
        Singleton property cadd_version, to set the globally available CADD version parsed from either the CADD file or
        from the command line arguments. Raises TypeError if not supplied with a float or None.

        :param value: float
        """
        pass

    @property
    def grch_build(self):
        """
        Getter for setter grch_build

        :return: integer
        """
        return self._grch_build

    @grch_build.setter
    def grch_build(self, value):
        """
        Singleton property grch_build, to set the globally available GRCh build parsed from either the CADD file or
        from the command line arguments. Raises TypeError if not supplied with an integer or None.

        :param value: integer
        """
        pass

    @property
    def cadd_features(self):
        """
        Getter for setter cadd_features

        :return: list
        """
        return self._cadd_features

    @cadd_features.setter
    def cadd_features(self, value):
        """
        Singleton property cadd_features, to set the globally available CADD features parsed in the imputer for the
        preprocessor and predictor. Raises TypeError if not supplied with a list.

        :param value: list
        """
        pass

    @property
    def force(self):
        """
        Getter for setter force

        :return: boolean
        """
        return self._force

    @force.setter
    def force(self, value):
        """
        Singleton property force, to tell the exporter to overwrite an already existing output file.
        Raises TypeError if not supplied with a boolean.

        :param value: boolean
        """
        pass

    @property
    def verbose(self):
        """
        Getter for setter verbose

        :return: boolean
        """
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        """
        Singleton property verbose, to print more (debug) messages during the process. Raises TypeError if not
        supplied with a boolean.

        :param value: boolean
        """
        pass

    @property
    def enable_logfile(self):
        """
        Getter for setter enable_logfile

        :return: boolean
        """
        return self._enable_logfile

    @enable_logfile.setter
    def enable_logfile(self, value):
        """
        Singleton property enable_logfile, to tell the logger whenever a logfile should be made or if everything
        should be piped to STDout and STDerr. Raises TypeError if not supplied with a boolean.

        :param value: boolean
        """
        pass

    @property
    def critical_logging_only(self):
        """
        Getter for setter critical_logging_only

        :return: boolean
        """
        return self._critical_logging_only

    @critical_logging_only.setter
    def critical_logging_only(self, value):
        """
        Singleton property critical_logging_only, to tell the logger to only log CRITICAL loglevel events to file /
        STDout and STDerr. Raises TypeError if not supplied with a boolean.

        :param value: boolean
        """
        pass

    @property
    def output_filename(self):
        return self._output_filename

    @output_filename.setter
    def output_filename(self, value):
        pass

    def __new__(cls):
        """
        Class method to set CapiceManager instance
        :return: instance
        """
        if not CapiceManager.instance:
            CapiceManager.instance = CapiceManager.__CapiceManager()
        return CapiceManager.instance

    def __init__(self):
        """
        __init__ method to set instance to CapiceManager.__CapiceManager()
        """
        if not CapiceManager.instance:
            CapiceManager.instance = CapiceManager.__CapiceManager()

    def __getattr__(self, name):
        """
        Method to return the value of the named attribute of name
        :param name: str
        :return: str
        """
        return getattr(self.instance, name)
