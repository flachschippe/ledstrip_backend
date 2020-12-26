from animations.parameter import ParameterBase


class ColorParameter(ParameterBase):
    def __init__(self, value):
        self._value = value
        pass

    @staticmethod
    def from_string(value_as_string):
        color = (int(value_as_string[-6:-4], 16), int(value_as_string[-4:-2], 16), int(value_as_string[-2:], 16))
        return ColorParameter(color)

    def __str__(self):
        return "#%02x%02x%02x" % (self._value[0], self._value[1], self._value[2])

    def get_type(self):
        return "color"
