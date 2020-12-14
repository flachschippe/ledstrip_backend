from ledstripbase import LedstripBase
from PIL import Image, ImageDraw


class GifWriterLedstrip(LedstripBase):
    def __init__(self, pixel_count, update_rate):
        self.__update_rate = update_rate
        self._pixel_count = pixel_count
        self.__led_size = 20
        self.__images = []
        pass

    def write_pixels(self, pixel_data):
        image = Image.new('RGB', (self.__led_size * self._pixel_count + self._pixel_count, 21))
        draw = ImageDraw.Draw(image)
        x = 0
        for pixel in pixel_data:
            draw.rectangle([(x, 0), (x + self.__led_size, self.__led_size)],
                           fill=(pixel[0], pixel[1], pixel[2]),
                           outline="white")
            x += 1 + self.__led_size
        self.__images.append((image))

    def shutdown(self):
        if len(self.__images) > 0:
            self.__images[0].save('leds.gif',
                                  save_all=True,
                                  append_images=self.__images[1:],
                                  optimize=False, duration=self.__update_rate * 1000, loop=0)

    def get_pixel_count(self):
        return self._pixel_count
