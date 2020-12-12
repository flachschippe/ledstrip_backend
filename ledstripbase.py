

class LedstripBase:
    def __init__(self, pixel_count):
        self._pixel_count = pixel_count
        pass

    def write_pixels(self, pixel_data):
        pass

    def delay(self):
        pass

    def get_pixel_count(self):
        pass