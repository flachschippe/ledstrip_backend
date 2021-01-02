import copy

import numpy as np

from animations.parameter.integerparameter import IntegerParameter


class Animation:
    def __init__(self, length):
        self._length = length
        self._parameters = self._get_default_parameters()

    def _init(self):
        self._oversampling = self._parameters["oversampling"].get_value()
        self._pixel_data = np.zeros((3, self._length * self._oversampling), dtype=int)

    def _get_default_parameters(self):
        return {"oversampling": IntegerParameter(1)}

    def increment(self):
        pass

    def get_pixel_data(self):
        reshaped_pixel_data = self._pixel_data.reshape((3, -1, self._oversampling))
        return reshaped_pixel_data.mean(axis=2).T.astype(int)

    def get_parameters(self):
        return self._parameters

    def set_parameters(self, parameters):
        default_parameters = self._get_default_parameters()
        for default_parameter_name in default_parameters.keys():
            if default_parameter_name not in parameters:
                parameters[default_parameter_name] = default_parameters[default_parameter_name]
        self._parameters = parameters
        self._init()

    def get_name(self):
        return str(self.__class__.__name__).lower()

    def clone(self):
        return copy.copy(self)
