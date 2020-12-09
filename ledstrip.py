from rpi_ws281x import *
import threading
import time
import numpy as np

class Animation:
    def __init__(self, ledstrip):
        self.ledstrip = ledstrip
        self.pixel_data = [0] * self.ledstrip.get_pixel_count()

    def increment(self):
        pass

class Walk(Animation):
    def __init__(self, ledstrip):
        Animation.__init__(self, ledstrip)
        self.counter = 0
        pass

    def increment(self):

        self.counter = self.count + 1 if self.count < self.ledstrip.get_pixel_count() else 0
        self.pixel_data[self.counter] = Color(10, 10, 10)



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
            pixel_data_accu = [0] * self.get_pixel_count()
            for animation in self.running_animations:
                animation.increment()
                pixel_count = 0
                for pixel in animation.pixel_data:
                    pixel_data_accu[pixel_count] = pixel
                    pixel_count += 1
                self.write_pixels(pixel_data_accu)
                time.sleep(.5)
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
                self.pixels[ledno] = pixelvalue
                ledno += 1
            self.strip.show()

    def write_pixel(self, ledno, pixelvalue):
        with self.pixel_lock:
            self.pixels[ledno] = pixelvalue
            self.strip.show()