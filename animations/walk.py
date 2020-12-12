import numpy as np

from animations.animation import Animation


class Walk(Animation):
    def __init__(self, length):
        Animation.__init__(self, length)
        self._init(20)
        self.counter = 0
        dot_length = 3 * self._oversampling
        dot_color_red = np.interp(np.linspace(0, 2, dot_length), [0, 1, 2], [0, 100, 0])
        dot_color_green = np.zeros(dot_length)
        dot_color_blue = np.zeros(dot_length)
        point = np.array([dot_color_red, dot_color_green, dot_color_blue], dtype=int)
        self._pixel_data[:, 0:dot_length] = point
        pass

    def increment(self):
        self._pixel_data = np.roll(self._pixel_data, 1, axis=1)

