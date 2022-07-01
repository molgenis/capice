class ColumnUtils:
    """
    Utility class for columns.
    """

    def __init__(self):
        self.specified_columns = set()

    def get_specified_columns(self):
        """
        Getter for specified columns
        :return: list of specified columns
        """
        return self.specified_columns

    def set_specified_columns(self, specified_columns):
        """
        Setter for specified columns
        :param specified_columns: list
        """
        self.specified_columns = set(specified_columns)

    def add_to_specified_columns(self, columns):
        """
        Adds column(s) to the set of specified columns.
        :param columns: string/int/float or list/tuple/set
        """
        if type(columns) in [str, int, float]:
            columns = [columns]
        for column in columns:
            self.specified_columns.add(column)

    def column_in_specified_columns(self, column):
        """
        Checks whether column is in specified columns
        :param column: string
        :return: boolean
        """
        return column in self.specified_columns

    def get_missing_diff_with(self, columns):
        """
        Get the list of columns missing from the presented columns,
        compared to the specified columns
        :param columns: list of columns
        :return: list
        list of columns that are in the specified columns (specified_columns),
        but not in the presented ones (columns)
        """
        return list(self.specified_columns - set(columns))
