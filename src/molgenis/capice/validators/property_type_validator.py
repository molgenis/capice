class PropertyTypeValidator:
    def validate_property(self, value: object, expected_type: type, include_none: bool = False):
        """
        Logger method to raise a TypeError when a Property is not set correctly.

        :param value: value to be checked
        :param expected_type: type the value should match
        :param include_none: whenever None should be allowed
        """
        if isinstance(value, bool):
            if type(value) != expected_type:
                self._check_none(expected_type, value, include_none)

        elif not isinstance(value, expected_type):
            self._check_none(expected_type, value, include_none)

    def _check_none(self, expected_type, value, include_none):
        if include_none:
            if value is not None:
                self._raise_type_error(expected_type, value)
        else:
            self._raise_type_error(expected_type, value)

    @staticmethod
    def _raise_type_error(expected_type, value):
        error_message = "Expected variable type %s but got %s"
        raise TypeError(error_message % (expected_type, type(value)))
