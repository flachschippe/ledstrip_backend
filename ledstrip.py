from rpi_ws281x import *
import threading
import time
import numpy as np

class Animation:
    def __init__(self, ledstrip):
        self.ledstrip = ledstrip
        self.pixel_data = np.zeros((ledstrip.get_pixel_count(), 3), dtype=int)

    def increment(self):
        pass

class Walk(Animation):
    def __init__(self, ledstrip):
        Animation.__init__(self, ledstrip)
        self.counter = 0
        self.pixel_data[0] = [1,0,0]
        self.pixel_data[1] = [3,0,0]
        self.pixel_data[2] = [10,0,0]
        self.pixel_data[3] = [3,0,0]
        self.pixel_data[4] = [1,0,0]
        pass

    def increment(self):
        self.pixel_data = np.roll(self.pixel_data, 1, axis=0)




class Ledstrip:
    def __init__(self, num, pin):
        self.pixel_count = num
        self.strip = PixelStrip(self.pixel_count, 18)
        self.strip.begin()
        self.pixels = self.strip.getPixels()
        self.pixel_lock = threading.Lock()
        self.running_animations = []
        self.available_animations = {"walk" : Walk(self)}
        self.animation_runner = threading.Thread(target=self.run_animation)

    def start_animation(self, animation_name):
        animation = self.available_animations[animation_name]
        assert(animation is not None)
        self.running_animations.append(animation)
        if not self.animation_runner.is_alive():
            self.animation_runner.start()

    def run_animation(self):
        while len(self.running_animations) > 0:
            pixel_data_accu = np.zeros((self.get_pixel_count(),3), dtype=int)
            for animation in self.running_animations:
                animation.increment()
                pixel_data_accu += animation.pixel_data
                self.write_pixels(pixel_data_accu)
                time.sleep(.05)
        pass

    def get_pixel_count(self):
        return self.pixel_count

    def set_pixel(self, pixel_no, color):
        assert(pixel_no < self.pixel_count)
        self.write_pixel(pixel_no, color)
        self.strip.show()

    def write_pixels(self, pixeldata):
        with self.pixel_lock:
            ledno = 0
            for pixelvalue in pixeldata:
                self.pixels[ledno] = Color(int(pixelvalue[0]), int(pixelvalue[1]), int(pixelvalue[2]))
                ledno += 1
            self.strip.show()

    def write_pixel(self, ledno, pixelvalue):
        with self.pixel_lock:
            self.pixels[ledno] = pixelvalue
            self.strip.show()