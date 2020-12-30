import json

from animations.parameter import ParameterBase


class IntegerParameter(ParameterBase):
    def __init__(self, value, minimum=None, maximum=None):
        super().__init__(value)
        self._value = value
        self._minimum = minimum
        self._maximum = maximum

    @staticmethod
    def from_string(value_as_string):
        return IntegerParameter(int(value_as_string))

    def get_type(self):
        return "integer"

    def to_dict(self):
        result = super().to_dict()
        result["minimum"] = self._minimum
        result["maximum"] = self._maximum
        return result
