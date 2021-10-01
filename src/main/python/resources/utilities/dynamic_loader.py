import os
from src.main.python.core.logger import Logger
from src.main.python.resources.utilities.utilities import importer, load_modules
from src.main.python.resources.models.training_preprocessor import \
    TrainPreprocessor


class DynamicLoader:
    def __init__(self, required_attributes: list, path):
        """
        Dynamic Loader for both the imputer and preprocessor

        :param required_attributes: list, list containing all the required
        attritubes the loaded modules have to have.
        :param path: Path-like, path to the potential modules.

        Use `load_impute_preprocess_modules()` to load the modules required for
        the imputer and preprocessor. Use `load_manual_annotators()` to load
        the manual VEP annotation processors.
        """
        self.log = Logger().logger
        self.path = path
        self._check_dir_exists()
        self.required_attributes = required_attributes
        self.modules = {}
        self.module = None

    def load_impute_preprocess_modules(self, vep_version, grch_build,
                                       overwrite, train=False):
        """
        Load the modules within path and match the (if set) overwrite or the
        supplied VEP version and GRCh build for the Imputer or Preprocessor.

        :param vep_version: float, the VEP version used to create the input data
        :param grch_build: int, the GRCh build used
        :param overwrite: str or None, overwrite argument for either the
        imputer of preprocessor
        :param train: bool, returns the TrainPreprocessor() immediately if True

        :return: dict(path, obj), dictionary of the path and initialized class
        in path.

        :raises: FileNotFoundError, if no match can be found.
        """
        if train:
            return TrainPreprocessor()
        else:
            # 2 more attributes are required if not present in
            # required_attributes
            extra_required_attributes = [
                'supported_vep_version',
                'supported_grch_build'
            ]
            # Required to preserve the original list of required attributes
            copy_required_attributes = self.required_attributes[:]
            for attribute in extra_required_attributes:
                if attribute not in copy_required_attributes:
                    copy_required_attributes.append(attribute)

            self._load_modules(copy_required_attributes)
            self._load_correct_module(overwrite, vep_version, grch_build)
            return self.module

    def _load_correct_module(self, overwrite, vep_version, grch_build):
        if overwrite:
            for path, module in self.modules.items():
                if module.name == overwrite:
                    self.log.info(
                        'Overwrite successful for: %s, '
                        'located at: %s', overwrite, path
                    )
                    self.module = module
                    return
            # If no match is found, trigger error.
            self._raise_module_not_found_error(overwrite)
        else:
            for path, module in self.modules.items():
                module_vep = module.supported_vep_version
                module_grch = module.supported_grch_build
                if module_vep == vep_version and module_grch == grch_build:
                    self.log.info(
                        'Module containing VEP version %s and GRCh build %s '
                        'successfully identified: %s, located at: %s',
                        vep_version,
                        grch_build,
                        module.name,
                        path
                    )
                    self.module = module
                    return
            # If no match is found, trigger error.
            self._raise_no_module_found_error()

    def load_manual_annotators(self):
        """
        Load the VEP annotation modules within path.

        :return: list, list containing all the usable VEP modules within path.

        :raises: FileNotFoundError, if no VEP annotation module is found within
        path.
        """
        self._load_modules()
        # Since the manual annotator doesn't require VEP version, GRCh build or
        # overwrite, this loading is done.
        return self.modules.values()

    def _load_modules(self, required_attributes=None):
        self._check_dir_exists()
        if required_attributes:
            set_required = required_attributes
        else:
            set_required = self.required_attributes
        modules = load_modules(self.path)
        self._check_n_modules(modules)
        imported_modules = importer(modules)
        for path, module in imported_modules.items():
            if all(item in dir(module) for item in set_required):
                self.modules[path] = module
        self._check_n_modules(self.modules)
        self.log.info('Successfully loaded %s modules.', len(self.modules))

    def _check_dir_exists(self):
        if not os.path.exists(self.path):
            error_message = "%s is not a path!"
            self.log.critical(error_message, self.path)
            raise OSError(error_message % self.path)

    def _check_n_modules(self, modules_dict):
        if len(modules_dict) < 1:
            self._raise_no_module_found_error()

    def _raise_no_module_found_error(self):
        error_message = "No usable modules are found within %s!"
        self.log.critical(error_message, self.path)
        raise FileNotFoundError(error_message % self.path)

    def _raise_module_not_found_error(self, overwrite):
        error_message = "No module overwrite with %s can be found within %s!"
        self.log.critical(error_message, overwrite, self.path)
        raise FileNotFoundError(error_message % (overwrite, self.path))
