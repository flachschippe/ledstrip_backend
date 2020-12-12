import threading

from injector import inject
import numpy as np

from animations.walk import Walk


# noinspection SpellCheckingInspection
from ledstripbase import LedstripBase


class LedstripController:
    @inject
    def __init__(self, ledstrip : LedstripBase):
        self.__pixel_count = ledstrip.get_pixel_count()
        self.__ledstrip = ledstrip
        self.__running_animations = []
        self.__available_animations = {"walk": lambda: Walk(self.__pixel_count)}
        self.__animation_runner = threading.Thread(target=self.__run_animation)

    def start_animation(self, animation_name):
        animation = self.__available_animations[animation_name]
        assert (animation is not None)
        self.__running_animations.append(animation())
        if not self.__animation_runner.is_alive():
            self.__animation_runner.start()

    def __run_animation(self):
        while len(self.__running_animations) > 0:
            pixel_data_accu = np.zeros((self.__pixel_count, 3), dtype=int)
            for animation in self.__running_animations:
                animation.increment()
                pixel_data_accu += animation.get_pixel_data()
                self.__ledstrip.write_pixels(pixel_data_accu)
                self.__ledstrip.delay()
        pass


