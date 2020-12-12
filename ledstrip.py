import threading
import time

from rpi_ws281x import *

from ledstripbase import LedstripBase


class Ledstrip(LedstripBase):
    def __init__(self, pixel_count):
        LedstripBase.__init__(self, pixel_count)
        self.__strip = PixelStrip(self._pixel_count, 18)
        self.__strip.begin()
        self.__pixels = self.__strip.getPixels()
        self.__pixel_lock = threading.Lock()
        pass

    def write_pixels(self, pixel_data):
        with self.__pixel_lock:
            ledno = 0
            for pixelvalue in pixel_data:
                self.__pixels[ledno] = Color(int(pixelvalue[0]), int(pixelvalue[1]), int(pixelvalue[2]))
                ledno += 1
            self.__strip.show()

    def delay(self):
        time.sleep(.02)
