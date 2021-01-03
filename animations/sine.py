import numpy as np

from animations import Animation
from animations.parameter.colorparameter import ColorParameter
from animations.parameter.integerparameter import IntegerParameter


class Sine(Animation):
    def __init__(self, length):
        super().__init__(length)
        self.__counter = 0.0
        self._init()
        pass

    def increment(self):
        oversampling = self._parameters["oversampling"].get_value()

        self.__counter += (1.0 / oversampling)
        self.__write_sine()

    def _init(self):
        Animation._init(self)
        self.__write_sine()

    def __write_sine(self):
        colors = np.array([self._parameters["color"].get_value()]).T
        period_count = self._parameters["period_count"].get_value()
        pixel_data_len = self._pixel_data.shape[1]
        x = np.linspace([0] * 3, [2 * np.pi * period_count] * 3, num=pixel_data_len).T + self.__counter

        sine = (np.sin(x))
        sine += 1.1
        sine *= colors
        self._pixel_data = sine.astype(np.uint8)
        i = 1

    def _get_default_parameters(self):
        return {"period_count": IntegerParameter(3, 1, 10),
                "color": ColorParameter([0x10, 0x00, 0x00]),
                "oversampling": IntegerParameter(10, 1, 50)}
