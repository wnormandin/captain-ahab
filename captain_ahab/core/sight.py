from numpy import array
from PIL import ImageGrab
from cv2 import cv2 as cv
from typing import Union
from ..utils.constants import ImageRegistry, TriggerColors


class Eyes:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._w = width
        self._h = height
        self._current_view = None
        self._known_images = {}
        self._known_triggers = {}
        self._variance = 6

    @property
    def visual_field(self):
        return self._x, self._y, self._w, self._h

    def sample(self, target_field=None):
        # Sample the field of vision
        base_image = ImageGrab.grab(bbox=target_field or self.visual_field)
        # Convert color for match
        self._current_view = cv.cvtColor(array(base_image), cv.COLOR_RGB2BGR)

    def look(self, target_field=None) -> Union[ImageRegistry, TriggerColors, None]:
        self.sample(target_field=target_field)

        for image_key, image in self._known_images.items():
            found = cv.matchTemplate(self._current_view, image, cv.TM_CCOEFF_NORMED)
            if found >= 0.75:
                return ImageRegistry[image_key]

        for w in range(self._w):
            for h in range(self._h):
                pixel = self._current_view.getpixel((w, h))
                for trigger_key, trigger in self._known_triggers.items():
                    if self.match(pixel, trigger):
                        return TriggerColors[trigger_key]

    def match(self, pixel, color) -> bool:
        for n in range(3):
            if not (color[n] - self._variance) <= pixel[n] <= (color[n] + self._variance):
                return False
        return True

    def learn_image(self, image_key, image_path):
        self._known_images[image_key] = cv.imread(image_path)

    def learn_trigger(self, trigger_key, trigger_rgb):
        self._known_triggers[trigger_key] = trigger_rgb
