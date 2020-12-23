from injector import inject
from animations import Animation
import numpy as np

from ledstripbase import LedstripBase


class AnimationRunnerBase:
    def __init__(self):
        self._animations = {}
        self.__next_animation_id = 0
        self._ledstrip = None

    def is_running(self):
        return False;

    def add_animation(self, animation: Animation):
        self._animations[self.__next_animation_id] = animation
        new_animation_id = self.__next_animation_id
        self.__next_animation_id += 1
        return new_animation_id

    def start(self, ledstrip: LedstripBase):
        self._ledstrip = ledstrip
        self._start()

    def _start(self):
        pass

    def _run_animation(self):
        pixel_data_accu = np.zeros((self._ledstrip.get_pixel_count(), 3), dtype=int)
        for animation in self._animations.values():
            animation.increment()
            pixel_data_accu += animation.get_pixel_data()
        self._ledstrip.write_pixels(pixel_data_accu)
        self._delay()

    def get_animations(self):
        return self._animations

    def _delay(self):
        pass
