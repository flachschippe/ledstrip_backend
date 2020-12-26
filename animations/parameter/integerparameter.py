import json

from animations.parameter import ParameterBase


class IntegerParameter(ParameterBase):
    def __init__(self, value):
        self._value = value
        pass

    @staticmethod
    def from_string(value_as_string):
        return IntegerParameter(int(value_as_string))

    def get_type(self):
        return "integer"

