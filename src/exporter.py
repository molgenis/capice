class Exporter:
    """
    Singleton class used to export the files produced by CAPICE.
    """
    class __Exporter:
        def __init__(self):
            # Prepare output folder
            self.out_dir = os.path.join(get_project_root_dir(),
                                        'model_export')

            # Setup init variables
            self.today = datetime.datetime.now()
            self.export = False

            # Output json
            self.output_file = self._create_output_filename()

            # Initialize logger
            self.log = Logger().get_logger()

        def set_export_command(self, export_command):
            """
            Method to set the export command to -export command line argument.
            :param export_command: bool
            """
            if not isinstance(export_command, bool):
                raise ValueError("Given argument must be boolean")
            self.export = export_command

            # Prepare output directory
            if self.export:
                prepare_output_dir(self.out_dir)

            self.log.debug("Export, command set to: {}".format(
                self.export))

        def export_prototypes(self, export_prototypes):
            """
            Exports prototypes to project root/model_export/
            :param export_prototypes: numpy.array([n_prototypes, n_features+1])
            """
            if self.export:
                export = pd.DataFrame(export_prototypes)
                export.to_csv(os.path.join(self.out_dir,
                                           'prototypes_{}.csv'.format(
                                               self.today.strftime(
                                                   "%d_%B_%Y_%H%M%S"))),
                              index=True, header=True)
                self.log.info("Exported prototypes matrix to: {}".format(
                    self.out_dir))

        def export_omega(self, omega_matrix):
            """
            Exports omega matrix to project root/model_export/
            :param omega_matrix: numpy.array([n_features, n_dim])
            """
            if self.export:
                export = pd.DataFrame(omega_matrix)
                export.to_csv(os.path.join(self.out_dir,
                                           'relevance_matrix_{}.csv'.format(
                                               self.today.strftime(
                                                   "%d_%B_%Y_%H%M%S"))),
                              index=True, header=True)
                self.log.info("Exported omega matrix to: {}".format(
                    self.out_dir))

        def export_result_metrics(self, results):
            """
            Exports the result metrics put in results
            :param results: array-like
            """
            if self.export:
                export = pd.DataFrame(results)
                export.to_csv(os.path.join(self.out_dir,
                                           'export_metrics_{}.csv'.format(
                                               self.today.strftime(
                                                   "%d_%B_%Y_%H%M%S"))),
                              index=False, header=True)
                self.log.info("Exported result metrics to: {}".format(
                    self.out_dir))

        def add_setting(self, key, value):
            """
            Adds imputation/split/model setting to application_settings.json
            :param key: object.get_name()
            :param value: object.settings
            """
            if self.export:
                output = {key: value}
                if not check_file_exists(self.output_file):
                    with open(self.output_file, 'wt') as f:
                        json.dump(output, f)
                else:
                    with open(self.output_file, 'r') as f:
                        data = json.load(f)
                    data[key] = value
                    with open(self.output_file, 'wt') as f:
                        json.dump(data, f)
                self.log.info("Added setting for {} to {}".format(
                    key, self.output_file
                ))

        def _create_output_filename(self):
            return os.path.join(self.out_dir,
                                'application_settings_{}.json'.format(
                                    self.today.strftime("%d_%B_%Y_%H%M%S")))

        def is_export(self):
            """
            Returns the export boolean.
            :return: boolean
            """
            return self.export

    instance = None

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

    def is_file_duplicated(self, file_loc, file_name, file_extension):

        pass
