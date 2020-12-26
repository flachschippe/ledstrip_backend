import json


class ParameterBase:
    def __init__(self, value):
        self._value = value
        pass

    @staticmethod
    def from_string(value_as_string):
        pass

    def set_value(self, value):
        self._value = value

    def get_value(self):
        return self._value

    def __str__(self):
        return str(self._value)

    def get_type(self):
        pass

    def get_default_value(self):
        pass

    def to_dict(self):
        return {"type": self.get_type(), "value": str(self)}
