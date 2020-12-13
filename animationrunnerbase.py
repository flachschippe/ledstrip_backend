from injector import inject
from animations.animation import Animation
import numpy as np

from ledstripbase import LedstripBase


class AnimationRunnerBase:
    @inject
    def __init__(self):
        self.__animations = []
        self.__ledstrip = None

    def is_running(self):
        return False;

    def add_animation(self, animation: Animation):
        self.__animations.append(animation)

    def start(self, ledstrip: LedstripBase):
        self.__ledstrip = ledstrip
        self._start()

    def _start(self):
        pass

    def _run_animation(self):
        while len(self.__animations) > 0:
            pixel_data_accu = np.zeros((self.__ledstrip.get_pixel_count(), 3), dtype=int)
            for animation in self.__animations:
                animation.increment()
                pixel_data_accu += animation.get_pixel_data()
                self.__ledstrip.write_pixels(pixel_data_accu)
                self._delay()

    def _delay(self):
        pass