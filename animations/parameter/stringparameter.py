from animations.parameter import ParameterBase


class StringParameter(ParameterBase):
    def __init__(self, value):
        self._value = value
        pass

    @staticmethod
    def from_string(value_as_string):
        return StringParameter(value_as_string)

    def get_type(self):
        return "string"
