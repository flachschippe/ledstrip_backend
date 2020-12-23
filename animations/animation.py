import numpy as np


class Animation:
    def __init__(self, length):
        self._length = length
        self._oversampling = 1
        self._parameters = {}

    def _init(self, oversampling=1):
        self._oversampling = oversampling
        self._pixel_data = np.zeros((3, self._length * self._oversampling), dtype=int)

    def increment(self):
        pass

    def get_pixel_data(self):
        reshaped_pixel_data = self._pixel_data.reshape((3, -1, self._oversampling))
        return reshaped_pixel_data.mean(axis=2).T.astype(int)

    def get_parameters(self):
        return self._parameters
