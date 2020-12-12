import threading
import numpy as np

from animations.walk import Walk
from ledstrip import Ledstrip


# noinspection SpellCheckingInspection
class LedstripController:
    def __init__(self, pixel_count, pin):
        self.pixel_count = pixel_count
        self.__ledstrip = Ledstrip(pixel_count)
        self.__running_animations = []
        self.__available_animations = {"walk": Walk(self.pixel_count)}
        self.__animation_runner = threading.Thread(target=self.__run_animation)

    def start_animation(self, animation_name):
        animation = self.__available_animations[animation_name]
        assert (animation is not None)
        self.__running_animations.append(animation)
        if not self.__animation_runner.is_alive():
            self.__animation_runner.start()

    def __run_animation(self):
        while len(self.__running_animations) > 0:
            pixel_data_accu = np.zeros((self.pixel_count, 3), dtype=int)
            for animation in self.__running_animations:
                animation.increment()
                pixel_data_accu += animation.get_pixel_data()
                self.__ledstrip.write_pixels(pixel_data_accu)
                self.__ledstrip.delay()
        pass


