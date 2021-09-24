from abc import abstractmethod


class PropertyChecker:
    def check_property(self, value: any, expected_type: any,
                       include_none: bool = False):
        """
        Logger method to raise a TypeError when a Property is not set correctly.

        :param value: value to be checked
        :param expected_type: type the value should match
        :param include_none: whenever None should be allowed
        """
        if not isinstance(value, expected_type):
            if include_none:
                if value is not None:
                    self._raise_type_error(expected_type, value)
            else:
                self._raise_type_error(expected_type, value)

    def _raise_type_error(self, expected_type, value):
        error_message = f"Expected variable type " \
                        f"{expected_type} but got {type(value)}"
        self._talk_to_logger(error_message)
        raise TypeError(error_message)

    @abstractmethod
    def _talk_to_logger(self, error_message):
        pass
