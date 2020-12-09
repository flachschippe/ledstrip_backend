from rpi_ws281x import *
import threading
import time

class Animation:
    def __init__(self, ledstrip):
        self.ledstrip = ledstrip
        self.thread = threading.Thread(target=self.run_animation)

    def start(self):
        self.thread.start()
        while True:
            self.run_animation()

    def run_animation(self):
        pass

class Walk(Animation):
    def __init__(self, ledstrip):
        Animation.__init__(self, ledstrip)
        self.counter = 0
        pass

    def run_animation(self):
        self.ledstrip.write_pixel(self.counter, Color(0,0,0))
        if self.counter < self.ledstrip.get_pixel_count():
            self.counter += 1
            self.ledstrip.write_pixel(self.counter, Color(10, 10, 10))
        else:
            self.counter = 0
        time.sleep(0.5)


class Ledstrip:
    def __init__(self, num, pin):
        self.pixel_count = num
        self.strip = PixelStrip(self.pixel_count, 18)
        self.strip.begin()
        self.pixels = self.strip.getPixels()
        self.pixel_lock = threading.Lock()

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