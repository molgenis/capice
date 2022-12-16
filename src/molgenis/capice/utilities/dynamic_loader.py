import os
from importlib import util

from molgenis.capice.core.logger import Logger


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
        self.modules: dict[str, object] = {}

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
        modules = self._load_modules_from_path(self.path)
        self._check_n_modules(modules)
        imported_modules = self._import(modules)
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

    @staticmethod
    def _load_modules_from_path(path):
        """
        Function to dynamically load in modules in the given path
        :param path: path to the modules
        :return: list
        """
        modules = []
        for module in os.listdir(path):
            module = os.path.join(path, module)
            if (module.endswith('.py') and not module.endswith('__.py')
                    and not module.endswith('abstract.py')):
                modules.append(module)
        return modules

    def _import(self, usable_modules: list[str]) -> dict[str, object]:
        """
        Function  to dynamically load in the modules using the
        import_module library.
        :param usable_modules: list of absolute paths to potential modules
        :return: list of usable modules
        """
        # For some reason, mypy wants this line to be Typed instead of the method.
        return_modules: dict[str, object] = {}
        for module in usable_modules:
            name = os.path.basename(module).split('.py')[0]
            spec = util.spec_from_file_location(name=name, location=module)
            loaded_module = self._process_spec(spec)
            if loaded_module and module not in return_modules.keys():
                return_modules[module] = loaded_module
        return return_modules

    @staticmethod
    def _process_spec(spec):
        return_spec = None
        loaded_spec = util.module_from_spec(spec)
        spec.loader.exec_module(loaded_spec)
        for attribute in dir(loaded_spec):
            if not attribute.startswith('Template') and not attribute.startswith('__'):
                get_attribute = getattr(loaded_spec, attribute)
                if ('name' in dir(get_attribute) and 'usable' in dir(get_attribute)
                        and get_attribute().usable is True):
                    return_spec = get_attribute()
        return return_spec
