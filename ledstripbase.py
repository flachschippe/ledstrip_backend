
class LedstripBase:
    def __init__(self, pixel_count):
        self._pixel_count = pixel_count
        pass

    def write_pixels(self, pixel_data):
        pass

    def get_pixel_count(self):
        return self._pixel_count

    def shutdown(self):
        pass