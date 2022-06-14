class ColumnChecker:
    def __init__(self):
        self.specified_columns = []

    def get_specified_columns(self):
        return self.specified_columns

    def set_specified_columns(self, specified_columns):
        self.specified_columns = specified_columns

    def add_to_specified_columns(self, column):
        if not self.column_in_specified_columns(column):
            self.specified_columns.append(column)

    def column_in_specified_columns(self, column):
        return column in self.specified_columns

    def get_missing_diff_with(self, columns):
        return list(set(self.specified_columns) - set(columns))