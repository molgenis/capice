from molgenis.capice.validators.property_type_validator import PropertyTypeValidator


class CapiceManager:
    """
    Global CAPICE manager, to keep track of variables used throughout
    the entirety of CAPICE.
    """

    class __CapiceManager:
        def __init__(self):
            self.property_checker = PropertyTypeValidator()
            self.loglevel = None
            self.critical_logging_only = False
            self.output_filename = ''

        @property
        def loglevel(self):
            return self._loglevel

        @loglevel.setter
        def loglevel(self, value):
            self.property_checker.validate_property(
                value=value, expected_type=int, include_none=True)
            self._loglevel = value

        @property
        def critical_logging_only(self):
            return self._critical_logging_only

        @critical_logging_only.setter
        def critical_logging_only(self, value):
            self.property_checker.validate_property(value=value, expected_type=bool)
            self._critical_logging_only = value

        @property
        def output_filename(self):
            return self._output_filename

        @output_filename.setter
        def output_filename(self, value):
            self.property_checker.validate_property(value=value, expected_type=str)
            self._output_filename = value

    instance = None

    @property
    def loglevel(self):
        """
        Getter for setter loglevel

        :return: None or int
        """
        return self._loglevel

    @loglevel.setter
    def loglevel(self, value):
        """
        Singleton property loglevel, to set the loglevel in int that will be
        used in the session of CAPICE.

        Raises TypeError if not supplied with int or None

        :param value: int or None
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
        Singleton property critical_logging_only,
        to tell the logger to only log CRITICAL loglevel events to file /
        STDout and STDerr.
        Raises TypeError if not supplied with a boolean.

        :param value: boolean
        """
        pass

    @property
    def output_filename(self):
        """
        Getter for setter output_filename

        :return: path-like
        """
        return self._output_filename

    @output_filename.setter
    def output_filename(self, value):
        """
        Singleton property output_filename,
        to set the output file name that CAPICE prediction will produce.

        :param value: path-like
        """
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
