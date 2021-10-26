from src.main.python.resources.checkers.property_checker import PropertyChecker
import os
from datetime import datetime


class CapiceManager:
    """
    Global CAPICE manager, to keep track of variables used throughout
    the entirety of CAPICE.
    """
    class __CapiceManager:
        def __init__(self):
            self.property_checker = PropertyChecker()
            self._now = datetime.now()
            self.overwrite_impute = None
            self.overwrite_model = None
            self.grch_build = None
            self.config_grch_build = None
            self.force = False
            self.loglevel = None
            self.critical_logging_only = False
            self.annotation_features = []
            self.output_filename = ''
            self.reference_genome = None
            self.vep_version = None
            self.config_vep_version = None
            self.config_loc = None

        @property
        def now(self):
            """
            Deprecated
            """
            return self._now

        @property
        def overwrite_impute(self):
            """
            Deprecated
            """
            return self._overwrite_impute

        @overwrite_impute.setter
        def overwrite_impute(self, value=None):
            """
            Deprecated
            """
            self.property_checker.check_property(value=value,
                                                 expected_type=str,
                                                 include_none=True)
            self._overwrite_impute = value

        @property
        def overwrite_model(self):
            """
            Deprecated
            """
            return self._overwrite_model

        @overwrite_model.setter
        def overwrite_model(self, value):
            """
            Deprecated
            """
            self.property_checker.check_property(value=value,
                                                 expected_type=str,
                                                 include_none=True)
            self._overwrite_model = value

        @property
        def grch_build(self):
            """
            Deprecated
            """
            return self._grch_build

        @grch_build.setter
        def grch_build(self, value):
            """
            Deprecated
            """
            self.property_checker.check_property(value=value,
                                                 expected_type=int,
                                                 include_none=True)
            self._grch_build = value

        @property
        def config_grch_build(self):
            """
            Deprecated
            """
            return self._config_grch_build

        @config_grch_build.setter
        def config_grch_build(self, value):
            """
            Deprecated
            """
            self.property_checker.check_property(value=value,
                                                 expected_type=int,
                                                 include_none=True)
            self._config_grch_build = value

        @property
        def annotation_features(self):
            """
            Deprecated
            """
            return self._annotation_features

        @annotation_features.setter
        def annotation_features(self, value):
            """
            Deprecated
            """
            self.property_checker.check_property(value=value,
                                                 expected_type=list)
            self._annotation_features = value

        @property
        def force(self):
            """
            Deprecated
            """
            return self._force

        @force.setter
        def force(self, value):
            """
            Deprecated
            """
            self.property_checker.check_property(value=value,
                                                 expected_type=bool)
            self._force = value

        @property
        def loglevel(self):
            return self._loglevel

        @loglevel.setter
        def loglevel(self, value):
            self.property_checker.check_property(value=value,
                                                 expected_type=int,
                                                 include_none=True)
            self._loglevel = value

        @property
        def critical_logging_only(self):
            return self._critical_logging_only

        @critical_logging_only.setter
        def critical_logging_only(self, value):
            self.property_checker.check_property(value=value,
                                                 expected_type=bool)
            self._critical_logging_only = value

        @property
        def output_filename(self):
            return self._output_filename

        @output_filename.setter
        def output_filename(self, value):
            self.property_checker.check_property(value=value, expected_type=str)
            self._output_filename = value

        @property
        def reference_genome(self):
            """
            Deprecated
            """
            return self._reference_genome

        @reference_genome.setter
        def reference_genome(self, value):
            """
            Deprecated
            """
            self.property_checker.check_property(value=value,
                                                 expected_type=str,
                                                 include_none=True)
            self._reference_genome = value

        @property
        def vep_version(self):
            """
            Deprecated
            """
            return self._vep_version

        @vep_version.setter
        def vep_version(self, value):
            """
            Deprecated
            """
            self.property_checker.check_property(value=value,
                                                 expected_type=float,
                                                 include_none=True)
            self._vep_version = value

        @property
        def config_vep_version(self):
            """
            Deprecated
            """
            return self._config_vep_version

        @config_vep_version.setter
        def config_vep_version(self, value):
            """
            Deprecated
            """
            self.property_checker.check_property(value=value,
                                                 expected_type=float,
                                                 include_none=True)
            self._config_vep_version = value

        @property
        def config_loc(self):
            """
            Deprecated
            """
            return self._config_loc

        @config_loc.setter
        def config_loc(self, value):
            """
            Deprecated
            """
            if value is not None and not os.path.isfile(value):
                raise FileNotFoundError('Given config location is not a file!')
            self._config_loc = value

    instance = None

    @property
    def now(self):
        """
        Deprecated
        """
        return self._now

    @now.setter
    def now(self, value):
        """
        Deprecated
        """
        pass

    @property
    def overwrite_impute(self):
        """
        Deprecated
        """
        return self._overwrite_impute

    @overwrite_impute.setter
    def overwrite_impute(self, value=None):
        """
        Deprecated
        """
        pass

    @property
    def overwrite_model(self):
        """
        Deprecated
        """
        return self._overwrite_model

    @overwrite_model.setter
    def overwrite_model(self, value):
        """
        Deprecated
        """
        pass

    @property
    def grch_build(self):
        """
        Deprecated
        """
        return self._grch_build

    @grch_build.setter
    def grch_build(self, value):
        """
        Deprecated
        """
        pass

    @property
    def config_grch_build(self):
        """
        Deprecated
        """
        return self._config_vep_version

    @config_grch_build.setter
    def config_grch_build(self, value):
        """
        Deprecated
        """
        pass

    @property
    def annotation_features(self):
        """
        Deprecated
        """
        return self._annotation_features

    @annotation_features.setter
    def annotation_features(self, value):
        """
        Deprecated
        """
        pass

    @property
    def force(self):
        """
        Deprecated
        """
        return self._force

    @force.setter
    def force(self, value):
        """
        Deprecated
        """
        pass

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

    @property
    def reference_genome(self):
        """
        Deprecated
        """
        return self._reference_genome

    @reference_genome.setter
    def reference_genome(self, value):
        """
        Deprecated
        """
        pass

    @property
    def vep_version(self):
        """
        Deprecated
        """
        return self._vep_version

    @vep_version.setter
    def vep_version(self, value):
        """
        Deprecated
        """
        pass

    @property
    def config_vep_version(self):
        """
        Deprecated
        """
        return self._config_vep_version

    @config_vep_version.setter
    def config_vep_version(self, value):
        """
        Deprecated
        """
        pass

    @property
    def config_loc(self):
        """
        Deprecated
        """
        return self._config_loc

    @config_loc.setter
    def config_loc(self, value):
        """
        Deprecated
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
