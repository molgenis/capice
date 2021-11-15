import os
from src.main.python.core.logger import Logger
from src.main.python.utilities.utilities import importer, load_modules


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
