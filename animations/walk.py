import numpy as np

from animations import Animation
from animations.parameter.colorparameter import ColorParameter
from animations.parameter.integerparameter import IntegerParameter


class Walk(Animation):
    def __init__(self, length):
        Animation.__init__(self, length)
        self.counter = 0
        self._init()
        pass

    def increment(self):
        self._pixel_data = np.roll(self._pixel_data, 1, axis=1)

    def _init(self):
        Animation._init(self)
        dot_length = self._parameters["dot_size"].get_value() * self._oversampling
        dot = np.interp(np.linspace(0, 2, dot_length), [0, 1, 2], [0, 100, 0])
        red, green, blue = self._parameters["color"].get_value()
        point = np.array([dot * red, dot * green, dot * blue], dtype=int)
        self._pixel_data[:, 0:dot_length] = point

    def _get_default_parameters(self):
        return {"dot_size": IntegerParameter(3),
                "color": ColorParameter([0x10, 0x00, 0x00]),
                "oversampling": IntegerParameter(10)}
