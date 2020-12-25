import numpy as np

from animations import Animation


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
        dot_length = self._parameters["dot_size"] * self._oversampling
        dot = np.interp(np.linspace(0, 2, dot_length), [0, 1, 2], [0, 100, 0])
        red, green, blue = self._get_colors()
        point = np.array([dot * red, dot * green, dot * blue], dtype=int)
        self._pixel_data[:, 0:dot_length] = point

    def _get_default_parameters(self):
        return {"dot_size": 3, "color": "#100000", "oversampling": 10}

    def _get_colors(self):
        color_string = self._parameters["color"];
        return int(color_string[-6:-5], 16), int(color_string[-4:-3], 16), int(color_string[-2:], 16)
