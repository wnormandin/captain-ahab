from numpy import array
from PIL import ImageGrab
from cv2 import cv2 as cv


class Eyes:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._w = width
        self._h = height
        self._current_view = None
        self._known_images = {}
        self._known_triggers = {}

    @property
    def visual_field(self):
        return self._x, self._y, self._w, self._h

    def sample(self, target_field=None):
        # Sample the field of vision
        base_image = ImageGrab.grab(bbox=target_field or self.visual_field)
        # Convert color for match
        self._current_view = cv.cvtColor(array(base_image), cv.COLOR_RGB2BGR)

    def look(self, target_field=None):
        self.sample(target_field=target_field)

    def learn_image(self, image_key, image_path):
        self._known_images[image_key] = cv.imread(image_path)

    def learn_trigger(self, trigger_key, trigger_rgb):
        self._known_triggers[trigger_key] = trigger_rgb
