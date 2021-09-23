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
            self.overwrite_impute = False
            self.overwrite_model = False
            self.grch_build = False
            self.config_grch_build = False
            self.force = False
            self.loglevel = None
            self._loglevel_meaning = {}
            self.critical_logging_only = False
            self.annotation_features = []
            self.output_filename = ''
            self.reference_genome = False
            self.vep_version = False
            self.config_vep_version = False
            self.config_loc = None

        @property
        def now(self):
            return self._now

        @property
        def overwrite_impute(self):
            return self._overwrite_impute

        @overwrite_impute.setter
        def overwrite_impute(self, value=None):
            self.property_checker.check_property(value=value,
                                                 expected_type=(str, bool))
            self._overwrite_impute = value

        @property
        def overwrite_model(self):
            return self._overwrite_model

        @overwrite_model.setter
        def overwrite_model(self, value):
            self.property_checker.check_property(value=value,
                                                 expected_type=(str, bool))
            self._overwrite_model = value

        @property
        def grch_build(self):
            return self._grch_build

        @grch_build.setter
        def grch_build(self, value):
            self.property_checker.check_property(value=value,
                                                 expected_type=(int, bool))
            self._grch_build = value

        @property
        def config_grch_build(self):
            """
            Getter for setter config_grch_build

            :return: int
            """
            return self._config_grch_build

        @config_grch_build.setter
        def config_grch_build(self, value):
            self.property_checker.check_property(value=value,
                                                 expected_type=(int, bool))
            self._config_grch_build = value

        @property
        def annotation_features(self):
            return self._annotation_features

        @annotation_features.setter
        def annotation_features(self, value):
            self.property_checker.check_property(value=value,
                                                 expected_type=list)
            self._annotation_features = value

        @property
        def force(self):
            return self._force

        @force.setter
        def force(self, value):
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
        def loglevel_meaning(self):
            return self._loglevel_meaning

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
            return self._reference_genome

        @reference_genome.setter
        def reference_genome(self, value):
            self.property_checker.check_property(value=value,
                                                 expected_type=(bool, str))
            self._reference_genome = value

        @property
        def vep_version(self):
            return self._vep_version

        @vep_version.setter
        def vep_version(self, value):
            self.property_checker.check_property(value=value,
                                                 expected_type=float)
            self._vep_version = value

        @property
        def config_vep_version(self):
            return self._config_vep_version

        @config_vep_version.setter
        def config_vep_version(self, value):
            self.property_checker.check_property(value=value,
                                                 expected_type=(float, bool))
            self._config_vep_version = value

        @property
        def config_loc(self):
            return self._config_loc

        @config_loc.setter
        def config_loc(self, value):
            if value is not None:
                if not os.path.isfile(value):
                    raise FileNotFoundError(
                        'Given config location is not a file!'
                    )
            self._config_loc = value

    instance = None

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
        Singleton property now, to set a datetime instance of when program
        instance started.

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
        Singleton property overwrite_impute, to set a string for the imputer to
        overwrite the VEP version and genome
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
        Singleton property overwrite_model, to set a string for the
        preprocessor and predictor to overwrite the
        VEP version and genome build. Raises a TypeError if not supplied with a
        string or False.

        :param value: False or string
        """
        pass

    @property
    def grch_build(self):
        """
        Getter for setter grch_build

        :return: int
        """
        return self._grch_build

    @grch_build.setter
    def grch_build(self, value):
        """
        Singleton property grch_build, to set the definitive GRCh build to be used.
        Raises TypeError if not supplied with an integer or None.

        :param value: int
        """
        pass

    @property
    def config_grch_build(self):
        """
        Getter for setter config_grch_build

        :return: int
        """
        return self._config_vep_version

    @config_grch_build.setter
    def config_grch_build(self, value):
        """
        Singleton property config_grch_build,
        to set the GRCh build present in the config.
        Raises TypeError if not supplied with an integer or False.

        :param value: int
        """
        pass

    @property
    def annotation_features(self):
        """
        Getter for setter annotation_features

        :return: list
        """
        return self._annotation_features

    @annotation_features.setter
    def annotation_features(self, value):
        """
        Singleton property annotation_features, to set the globally available
        annotation features parsed in the imputer for the
        preprocessor and predictor. Raises TypeError if not supplied with a
        list.

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
        Singleton property force, to tell the exporter to overwrite an already
        existing output file.
        Raises TypeError if not supplied with a boolean.

        :param value: boolean
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
    def loglevel_meaning(self):
        """
        Getter for the dictionary that contains the int of the loglevel and
        it's string level (for instance {0, 'NOTSET'})
        """
        return self._loglevel_meaning

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
        Getter for setter reference_genome

        :return: False or path-like
        """
        return self._reference_genome

    @reference_genome.setter
    def reference_genome(self, value):
        """
        Singleton property reference_genome,
        to set the location of the GRCh37 reference genome.

        :param value: False or path-like
        """
        pass

    @property
    def vep_version(self):
        """
        Getter for setter vep_version

        :return: float
        """
        return self._vep_version

    @vep_version.setter
    def vep_version(self, value):
        """
        Singleton property vep_version, to set the definitive VEP version to be used.

        :param value: float
        """
        pass

    @property
    def config_vep_version(self):
        """
        Getter for setter config_vep_version

        :return: float
        """
        return self._config_vep_version

    @config_vep_version.setter
    def config_vep_version(self, value):
        """
        Singleton property config_vep_version,
        to set the VEP version present in the config.
        Raises TypeError if not supplied with an integer or False.

        :param value: float
        """
        pass

    @property
    def config_loc(self):
        """
        Getter for seter config_loc

        return: str, path-like
        """
        return self._config_loc

    @config_loc.setter
    def config_loc(self, value):
        """
        Singleton property config_loc,
        to set the location of a custom config used in a CAPICE run.
        Raises FileNotFoundError if custom config does not exist
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
